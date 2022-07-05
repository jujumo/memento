#!/usr/bin/env python3
import argparse
import logging
import sys
from configparser import ConfigParser
import os.path as path
from typing import Optional

logger = logging.getLogger('snippet')


class VerbosityParsor(argparse.Action):
    """ accept debug, info, ... or theirs corresponding integer value formatted as string."""
    def __call__(self, parser, namespace, values, option_string=None):
        try:  # in case it represent an int, directly get it
            values = int(values)
        except ValueError:  # else ask logging to sort it out
            assert isinstance(values, str)
            values = logging.getLevelName(values.upper())
        setattr(namespace, self.dest, values)


def main():
    try:
        conf_parser = argparse.ArgumentParser(add_help=False)  # Turn off help, print all options in response to -h
        conf_parser.add_argument(
            '-c', '--conf_file',
            help="Specify config file", metavar="FILE")
        args, remaining_argv = conf_parser.parse_known_args()

        config = {}
        if args.conf_file:
            config_file = ConfigParser()
            config_file.read([args.conf_file])
            config = dict(config_file.items('Defaults'))

        # Parse rest of arguments
        parser = argparse.ArgumentParser(description='Description of the program.', parents=[conf_parser])
        parser.add_argument(
            '-v', '--verbose', nargs='?', default=logging.WARNING, const=logging.INFO, action=VerbosityParsor,
            help='verbosity level (debug, info, warning, critical, ... or int value) [warning]')
        parser.add_argument(
            '-i', '--input', metavar='FILE',
            help='input')
        parser.add_argument(
            '-o', '--output', metavar='FILE',
            help='output file')
        parser.set_defaults(**config)
        args = parser.parse_args(remaining_argv)

        logger.setLevel(args.verbose)
        logger.debug('config:\n' + '\n'.join(f'\t\t{k}={v}' for k, v in vars(args).items() if k != 'conf_file'))
        #########################
        # place your code here #
        ########################

    except Exception as e:
        logger.critical(e)
        if args.verbose <= logging.DEBUG:
            raise


if __name__ == '__main__':
    logger_formatter = logging.Formatter('%(name)s::%(levelname)-8s: %(message)s')
    logger_stream = logging.StreamHandler()  # logging.FileHandler(logfile)
    logger_stream.setFormatter(logger_formatter)
    logger.addHandler(logger_stream)
    main()
