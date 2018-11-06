#!/usr/bin/env python3
import logging
import os
import os.path as path
import re

import chocolatey_packages


def preprocessor(root_path, input_filepath, output_filepath):
    include_re = re.compile(r'include\:\:(?P<filepath>[^\[]*)')
    with open(path.join(root_path, input_filepath), 'r') as input_file:
        input_lines = input_file.readlines()

    with open(path.join(root_path, output_filepath), 'w') as output_file:
        for input_line in input_lines:
            include_match = include_re.match(input_line)
            if not include_match:
                # just copy
                output_file.write(input_line)
            else:
                included_filepath = include_match.groupdict()['filepath']
                with open(path.join(SCRIPT_PATH, included_filepath), 'r') as included_file:
                    included_lines = included_file.readlines()
                    included_lines = ''.join(included_lines)
                output_file.write(included_lines)

# process templates
SCRIPT_PATH = path.dirname(path.realpath(__file__))
preprocessor(SCRIPT_PATH, 'chocolatey.template.adoc', 'chocolatey.adoc')