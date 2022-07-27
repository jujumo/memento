#!/usr/bin/env python3
import argparse
import logging
import sys
from yaml import safe_load
import os.path as path
from typing import Optional

logger = logging.getLogger('snippet')


class Config(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        if name == 'verbose':  # convert verbose level to logging type (int)
            try:  # in case it represents an int, directly get it
                values = int(value)
            except ValueError:  # else ask logging to sort it out
                assert isinstance(value, str)
                value = logging.getLevelName(value.upper())

        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __repr__(self):
        return '\n'.join(f'\t\t{k}: {v}' for k, v in self.items())

    def update_from_args(self, args):
        self.update(vars(args).items())

    def set_defaults(self):
        {'verbose': 'info'}

    def check(self):
        pass


def main():
    config = Config()
    try:
        conf_parser = argparse.ArgumentParser(add_help=False)  # Turn off help, print all options in response to -h
        conf_parser.add_argument('-c', '--conf_file', help="Specify config file", metavar="FILE")
        args, remaining_argv = conf_parser.parse_known_args()
        if args.conf_file and path.isfile(args.conf_file):
            with open(args.conf_file, 'r') as f:
                config.update(safe_load(f))
        # Parse rest of arguments
        parser = argparse.ArgumentParser(description='Description of the program.', parents=[conf_parser])
        parser.set_defaults(**config)
        parser.add_argument(
            '-v', '--verbose', nargs='?', const='info',
            help='verbosity level (debug, info, warning, critical, ... or int value) [warning]')
        parser.add_argument(
            '-i', '--input', metavar='FILE',
            help='input')
        parser.add_argument(
            '-o', '--output', metavar='FILE',
            help='output file')
        args = parser.parse_args(remaining_argv)
        config.update_from_args(args)
        config.set_defaults()
        logger.setLevel(config.verbose)
        logger.debug('config:\n' + str(config))
        logger.info('info')
        #########################
        # place your code here #
        ########################

    except Exception as e:
        logger.critical(e)
        if config.verbose <= logging.DEBUG:
            raise


if __name__ == '__main__':
    logger_formatter = logging.Formatter('%(name)s::%(levelname)-8s: %(message)s')
    logger_stream = logging.StreamHandler()  # logging.FileHandler(logfile)
    logger_stream.setFormatter(logger_formatter)
    logger.addHandler(logger_stream)
    main()
