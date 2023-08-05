"""This is a main AmpioGateway implementation module."""

import asyncio
import logging
from serial_asyncio import create_serial_connection
from enum import Enum
from pyampio.can import AmpioCanProtocol
from pyampio.modules import ModuleManager


_LOG = logging.getLogger(__name__)


class GatewayState(Enum):
    """This is an enum class for Gateway State."""

    INIT = 0
    MODULE_DISCOVERY = 4
    MODULE_NAME_DISCOVERY = 5
    MODULE_DETAILS_DISCOVERY = 6
    ATTRIBUTE_NAMES_DISCOVERY = 7
    READY = 8


class AmpioGateway:
    """This is a AmpioGateway class handling the connection USB<->Ampio CAN bus."""

    def __init__(self, port=None, loop=None):
        """Initialize the :class: pyampio.AmpioGateway object.

        Args:
            port (str): The USB port path i.e. /dev/usb1
            loop: Asynction Event Loop

        """
        self._modules = ModuleManager()
        self._on_discovered_callbacks = []
        self._port = port
        self._loop = loop
        self._is_relevant = lambda can_id: True
        self._protocol_coro = create_serial_connection(
            loop, lambda: AmpioCanProtocol(
                on_connected=self.on_connected,
                on_can_broadcast_received=self.on_can_broadcast_received,
                on_can_data_received=self.on_can_data_received,
                is_relevant=self._is_relevant
            ), port, baudrate=115200
        )
        self.protocol = None
        self._state = GatewayState.INIT
        asyncio.ensure_future(self._protocol_coro, loop=self._loop)

    @property
    def state(self):
        """Return the current object state.

        Returns:
            GatewayState: The current gateway state.

        """
        return self._state

    @state.setter
    def state(self, value):
        """Set the object state."""
        _LOG.info("State change {}->{}".format(self._state.name, value.name))
        self._state = value

    def add_on_discovered_callback(self, callback):
        """Add the callback for On Discovered Event."""
        if callback not in self._on_discovered_callbacks:
            self._on_discovered_callbacks.append(callback)

    def remove_on_discovered_callback(self, callback):
        """Remove the callback for On Discovered Event."""
        try:
            self._on_discovered_callbacks.remove(callback)
        except ValueError:
            pass

    @asyncio.coroutine
    def on_discovered(self):
        """Fire the callback when all modules are fully discovered."""
        for callback in self._on_discovered_callbacks:
            yield callback(modules=self._modules)

    def discovery_finished(self):
        """Move to the Module Name Discovery phase when all module discovered."""
        _LOG.info("Total {} modules discovered".format(len(self._modules.modules)))
        self.state = GatewayState.MODULE_NAME_DISCOVERY
        self._loop.create_task(self.module_names_discovery())

    @asyncio.coroutine
    def on_connected(self, protocol):
        """Call on gateway connected event."""
        _LOG.debug("Connected")
        self.protocol = protocol
        self.state = GatewayState.MODULE_DISCOVERY
        self.protocol.send_module_discovery()
        self._loop.call_later(2, self.discovery_finished)
        # send discovery broadcast

    @asyncio.coroutine
    def on_can_broadcast_received(self, can_id, can_data):
        """Handle the broadcast frame."""
        if self.state == GatewayState.READY:
            can_data_str = " ".join(["{:02x}".format(c) for c in can_data])
            _LOG.debug("CAN IN: id={:08x} data=[{}]".format(can_id, can_data_str))
            self._modules.broadcast_received(can_id, can_data)

    @asyncio.coroutine
    def on_can_data_received(self, can_id, can_data):
        """Handle the data frame."""
        if self.state == GatewayState.MODULE_DISCOVERY:
            self._modules.add_module(can_id, can_data)
        elif self.state == GatewayState.MODULE_NAME_DISCOVERY:
            self._modules.update_name(can_id, can_data)
        elif self.state == GatewayState.MODULE_DETAILS_DISCOVERY:
            self._modules.update_details(can_id, can_data)

    @asyncio.coroutine
    def module_names_discovery(self):
        """Run the module names discovery phase."""
        for can_id, mod in self._modules.modules.items():
            # TODO: delegate to ModuleManager
            self.protocol.send_module_name_discovery(can_id)
            yield from self._modules.is_name_updated(can_id)
        _LOG.info("Module names discovered")
        self.state = GatewayState.MODULE_DETAILS_DISCOVERY
        self._loop.create_task(self.module_details_discovery())

    @asyncio.coroutine
    def module_details_discovery(self):
        """Run the module details discovery phase."""
        for can_id, mod in dict(self._modules.modules).items():
            self.protocol.send_module_details_discovery(can_id)
            yield from self._modules.is_details_updated(can_id)
        for can_id, mod in self._modules.modules.items():
            _LOG.info(mod)
        _LOG.info("Module details discovered")
        self.state = GatewayState.READY
        self._loop.create_task(self.on_discovered())
        # TODO(klstanie): Add the attribute names discovery logic
        # Attribute names discovery not implemented yet
        # self.state = GatewayState.ATTRIBUTE_NAMES_DISCOVERY
        # self._loop.create_task(self.attribute_names_discovery())

    @asyncio.coroutine
    def attribute_names_discovery(self):
        """Run the attribute names discovery phase."""
        for can_id, mod in dict(self._modules.modules).items():
            self.protocol.send_attribute_names_discovery(can_id)
            yield from self._modules.is_attribute_names_updated(can_id)
        for can_id, mod in self._modules.modules.items():
            _LOG.info(mod)
        _LOG.info("Attribute names discovered")

    def register_on_value_change_callback(self, can_id, attribute, index, callback):
        """Register the value changed callback."""
        self._modules.register_on_value_changed_callback(can_id, attribute, index, callback)

    def get_item_state(self, can_id, attribute, index):
        """Return the item state from ampio module."""
        return self._modules.get_state(can_id, attribute, index)

    def get_item_measurement_unit(self, can_id, attribute, index):
        """Return the item measurement unit."""
        return self._modules.get_measurement_unit(can_id, attribute, index)

    def get_module_name(self, can_id):
        """Return Ampio module name."""
        return self._modules.get_module(can_id).name

    def get_module_part_number(self, can_id):
        """Return Ampio module part number."""
        return self._modules.get_module(can_id).part_number
