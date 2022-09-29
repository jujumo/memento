#!/usr/bin/env python3
import argparse
import logging
import sys
from yaml import safe_load
import os.path as path
from typing import Optional

logger = logging.getLogger('snippet')


class Config(dict):
    def __getattr__(self, name):  # for ease of access, e.g. config.verbose
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __repr__(self):
        return '\n'.join(f'\t\t{k}: {v}' for k, v in self.items())

    def validate(self):
        # verbose
        verbose_level = self.get('verbose')
        verbose_level = 'warning' if verbose_level is None else verbose_level
        if verbose_level is not None:  # convert verbose level to logging type (int)
            try:  # in case it represents an int, directly get it
                verbose_level = int(verbose_level)
            except ValueError:  # else ask logging to sort it out
                assert isinstance(verbose_level, str)
                verbose_level = logging.getLevelName(verbose_level.upper())
            self['verbose'] = verbose_level


def main():
    config = Config()
    try:
        parser_conf_file = argparse.ArgumentParser(add_help=False)  # Turn off help, print all options in response to -h
        parser_conf_file.add_argument('-c', '--conf_file', help="Specify config file (yaml)", metavar="FILE")
        args, remaining_argv = parser_conf_file.parse_known_args()  # only retrieve the config file path from cli
        if args.conf_file and path.isfile(args.conf_file):
            with open(args.conf_file, 'r') as f:
                config.update(safe_load(f))
        # Parse rest of arguments
        parser = argparse.ArgumentParser(description='Description of the program.', parents=[parser_conf_file])
        parser.add_argument(
            '-v', '--verbose', nargs='?', const='info', type=str,
            help='verbosity level (debug, info, warning, critical, ... or int value) [warning]')
        parser.add_argument(
            '-i', '--input', metavar='FILE',
            help='input file')
        parser.add_argument(
            '-o', '--output', metavar='FILE',
            help='output file')
        args = parser.parse_args(remaining_argv)
        config.update(vars(args).items())
        config.validate()
        logger.setLevel(config.verbose)
        logger.debug('config:\n' + str(config))
        logger.critical('printing critical')
        logger.warning('printing warning')
        logger.info('printing info')
        logger.debug('printing debug')
        #########################
        # place your code here #
        ########################

    except Exception as e:
        logger.critical(e)
        if config.verbose <= logging.DEBUG:
            raise


if __name__ == '__main__':
    logger_formatter = logging.Formatter('%(name)s::%(levelname)-8s: %(message)s')
    logger_stream = logging.StreamHandler()  # or logging.FileHandler(logfile)
    logger_stream.setFormatter(logger_formatter)
    logger.addHandler(logger_stream)
    main()
