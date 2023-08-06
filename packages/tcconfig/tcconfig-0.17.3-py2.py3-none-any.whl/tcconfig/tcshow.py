#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys

import logbook
import subprocrunner

import simplejson as json

from ._argparse_wrapper import ArgparseWrapper
from ._common import (
    check_tc_command_installation,
    initialize_cli,
    verify_network_interface,
    write_tc_script,
)
from ._const import (
    VERSION,
    Tc,
    TcCommandOutput,
)
from ._error import NetworkInterfaceNotFoundError
from ._logger import logger
from .parser.shaping_rule import TcShapingRuleParser


def parse_option():
    parser = ArgparseWrapper(VERSION)

    group = parser.parser.add_argument_group("Traffic Control")
    group.add_argument(
        "-d", "--device", action="append", required=True,
        help="network device name (e.g. eth0)")
    group.add_argument(
        "--ipv6", dest="ip_version", action="store_const",
        const=6, default=4,
        help="""
        Display IPv6 shaping rules.
        Defaults to show IPv4 shaping rules.
        """)

    return parser.parser.parse_args()


def main():
    options = parse_option()

    initialize_cli(options)
    check_tc_command_installation()

    if options.tc_command_output != TcCommandOutput.NOT_SET:
        subprocrunner.SubprocessRunner.default_is_dry_run = True

    tc_param = {}
    for device in options.device:
        try:
            verify_network_interface(device)

            tc_param.update(TcShapingRuleParser(
                device, options.ip_version, options.tc_command_output, logger
            ).get_tc_parameter())
        except NetworkInterfaceNotFoundError as e:
            logger.debug(e)
            continue

    command_history = "\n".join(subprocrunner.SubprocessRunner.get_history())

    if options.tc_command_output == TcCommandOutput.STDOUT:
        print(command_history)
        return 0

    if options.tc_command_output == TcCommandOutput.SCRIPT:
        write_tc_script(
            Tc.Command.TCSHOW,
            command_history,
            filename_suffix="-".join(options.device))
        return 0

    logger.debug("command history\n{}".format(command_history))
    print(json.dumps(tc_param, indent=4))

    return 0


if __name__ == '__main__':
    sys.exit(main())
