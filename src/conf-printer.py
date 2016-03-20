#!/usr/bin/env python2
# -*- coding: utf-8 -*-


#
#  This file is part of Conf File Printer.
#
#  Conf File Printer is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Conf File Printer is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Conf File Printer. If not, see <http://www.gnu.org/licenses/>.
#
##


from __future__ import print_function

import argparse
import yaml
import sys
import traceback

import logging
logging.basicConfig(format="%(filename)s:%(lineno)s: %(message)s", level="DEBUG")
logger = logging.getLogger('root')

def getCLIArgs():
    mainHelpText = "This is printer of an option value from an YAML configuration file."

    parser = argparse.ArgumentParser(description=mainHelpText)
    subparsers = parser.add_subparsers(dest="requestedAction",
                                        title="Available commands",
                                        description="There are certain available commands.",
                                        help='Choose one of these commands.')

    parserBasic = subparsers.add_parser('print',
                                            help='Look up and print a value.')
    parserBasic.add_argument('--file',
                            dest="fileName",
                            required=True,
                            help="YAML file name to be used.")
    parserBasic.add_argument('--option',
                            dest='optionNamesChain',
                            required=True,
                            action='store',
                            nargs='+',
                            help="Sequence of space delimited names to look for in configuration file - path to a value inside configuration file.")

    parserTest = subparsers.add_parser('test',
                                            help='Will replace CLI arguments and do self-tests.')

    cliArgs = parser.parse_args()

    return cliArgs


def getFromDict(obj, wantedNamesChain):
    if isinstance(obj, dict):
        assert len(wantedNamesChain) > 0, "Wanted option names list chain length must be greater than 0."
        rootName = wantedNamesChain[0]
        for key in obj:
            if key == rootName:
                return getFromDict(obj[rootName],wantedNamesChain[1:])
    else:
        return obj


def printFromDict(obj, wantedNamesChain):
    dbgMessageTemplate = "For option '%s' found value '%s'."
    val = getFromDict(obj, wantedNamesChain)
    if isinstance(val, str):
        logger.debug( dbgMessageTemplate % (str(wantedNamesChain),str(val)))
        print(val)
    else:
        for item in val:
            logger.debug("For option '%s' found value '%s'." \
                            % (str(wantedNamesChain),str(item)))
            print(item)
    return val

def main(cliArgs):
    with open(cliArgs.fileName, 'r') as yamlfile:
        confInstance = yaml.load(yamlfile)
    return printFromDict(confInstance, cliArgs.optionNamesChain)


###
##
#


def replaceCLIArgs(ethalon):
    sys.argv = sys.argv[:1]
    sys.argv.append("print")

    sys.argv.append("--file")
    sys.argv.append(ethalon["file"])

    sys.argv.append("--option")
    sys.argv.extend(ethalon["path"])

def produceEthalons():
    ethalonPool = {"01":{}, "02":{}}

    ethalonPool["01"]["file"] = "conf-printer.test-ethalon-yaml"
    ethalonPool["01"]["path"] = ["file sync root", "moon", "ignore list"]
    ethalonPool["01"]["expected-value"] = str(["spot", "x-rays", "radiation"])

    ethalonPool["02"]["file"] = "conf-printer.test-ethalon-yaml"
    ethalonPool["02"]["path"] = ["file sync root", "moon", "dir chroot"]
    ethalonPool["02"]["expected-value"] = "/tmp/moon"

    return ethalonPool

def doTests(cliArgs):
    ethalonPool = produceEthalons()
    for ethalon in ethalonPool.values():
        replaceCLIArgs(ethalon)
        value = main(getCLIArgs())
        assert str(value) == ethalon["expected-value"], "Expected '%s' to be equal to '%s', but it is not." \
                                % (str(value), ethalon["expected-value"])


###
##
#


if __name__ == '__main__':
    try:
        cliArgs = getCLIArgs()
        if cliArgs.requestedAction == 'test':
            doTests(cliArgs)
        else:
            main(cliArgs)
    except Exception as e:
        traceback.print_exc(e)
