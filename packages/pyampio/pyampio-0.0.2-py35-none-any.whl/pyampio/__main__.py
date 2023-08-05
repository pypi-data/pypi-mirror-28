#!/usr/bin/env python
"""The ampio command line implementation."""

import asyncio
from pyampio.gateway import AmpioGateway
import logging


try:
    import click
except ImportError:
    print("Install click python package\n pip install click")
    exit()


def on_value_changed(modules, can_id, attribute, index, old_value, new_value, unit):
    """Handle the value changed event.

    Args:
        modules (ModuleManager): Module manager object
        can_id (int): CAN ID
        attribute (str): The attribute name i.e. input, bin_input, temperature, flag, etc.
        index (int): The attribute index (1-based)
        old_value: Old value
        new_value: New value
        unit (str): Unit

    """
    mod = modules.get_module(can_id)
    if mod:
        print("{:08x}/{:08x} {:16} {:32} {}({}) changed {}{}->{}{}".format(
            mod.physical_can_id, can_id, mod.part_number, mod.name, attribute, index, old_value, unit, new_value, unit)
        )


def on_discovered(modules):
    """Handle the on discovered event when discovery phase is finished."""
    for _, mod in modules.modules.items():
        print(mod)
    print("Discovered {} modules.".format(len(modules.modules)))
    print("Registering for value change events.")
    # Subscribe to all values
    for can_id, mod in modules.modules.items():
        modules.add_on_value_changed_callback(can_id=can_id, attribute=None, index=None, callback=on_value_changed)
    # modules.add_on_value_changed_callback(can_id=0x1ecc, attribute='bin_input', index=9, callback=on_value_changed)


log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "ERROR": logging.ERROR,
    "NONE": logging.NOTSET,
}


@click.command()
@click.option("--port", required=True, envvar='AMPIO_PORT', type=click.Path(),
              help='The USB interface full path i.e. /dev/cu.usbserial-DN01D1W1. '
                   'If no --port option provided the AMPIO_PORT environment variable is used.')
@click.option("--log-level", type=click.Choice(["NONE", "DEBUG", "INFO", "ERROR"]),
              show_default=True, default='ERROR',
              help='Logging level.')
def run(port, log_level):
    """Run main function."""
    formatter = "[%(asctime)s] %(levelname)s - %(message)s"
    logging.basicConfig(level=log_levels[log_level], format=formatter)

    loop = asyncio.get_event_loop()
    ampio_gw = AmpioGateway(port=port, loop=loop)
    ampio_gw.add_on_discovered_callback(on_discovered)
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    run()  # pylint: disable=no-value-for-parameter
