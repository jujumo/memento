#!/usr/bin/env python3
__author__ = 'jumo'

import argparse


def main():
    parser = argparse.ArgumentParser(description='Description of the program.')
    only_one = parser.add_mutually_exclusive_group()                                 # <1>
    only_one.add_argument('-q', '--quiet', action='store_true', help='quiet')        # <2>
    only_one.add_argument('-v', '--verbose', action='count', help='verbose message') # <3>
    parser.add_argument('-i', '--input', required=False, help='input')               # <4>
    parser.add_argument('-n', '--number', type=int, default=1, help='number')        # <5>
    parser.add_argument('-l', '--level', type=int, choices=[1, 2, 4], help='level')  # <6>
    parser.add_argument('-x', default=None, const='zip', nargs='?', help='format')   # <7>
    subparsers = parser.add_subparsers(help='sub-command help')
    # create the parser for the "a" command
    parser_a = subparsers.add_parser('aaa', help='a help')
    parser_a.add_argument('foo', help='bar help')
    # create the parser for the "b" command
    parser_b = subparsers.add_parser('bbb', help='b help')
    parser_b.add_argument('--baz', choices='321', help='baz help')

    #################################
    # some possible usages
    usages = [
        '-i input',
        '-i input -vvv',
        '-i input -n 10',
        '-i input -l 2',
        '-i input -x',
        '-i input -x tar',
        'aaa bar',
        'bbb --baz 1'
    ]
    # log it to file argparse_out.adoc
    from os.path import basename, dirname, join
    with open(join(dirname(__file__), 'argparse_out.adoc'), 'w') as fout:
        for usage in usages:
            fout.write('[source,bash]\n----\n> python {0} {1}\n'.format(basename(__file__), usage))
            fout.write(str(parser.parse_args(usage.split())))
            fout.write('\n----\n\n')
    #################################


if __name__ == '__main__':
    main()
