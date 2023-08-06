#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# Markdown_to_HTML                                                             #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program converts Markdown files to HTML recursively.                    #
#                                                                              #
# copyright (C) 2018 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help           display help message
    --version            display version and exit

    --directory=PATH     directory at which to recursively compile files
                         [default: .]
    
    --table_of_contents  include table of contents
    
    --CSS=PATH           path to CSS
                         [default: https://rawgit.com/wdbm/style/master/SS/newswire.css]
"""

import docopt
import os
import subprocess

name    = "Markdown_to_HTML"
version = "2018-01-17T1506Z"

def main(options):

    directory         = options["--directory"]
    table_of_contents = options["--table_of_contents"]
    CSS               = options["--CSS"]
    filepaths = filepaths_recursive(directory = directory)
    filepaths_compile = [filepath for filepath in filepaths if ".md" in filepath]
    for filepath in filepaths_compile:
        filepath_output                                     =\
            os.path.dirname(filepath)                       +\
            "/"                                             +\
            os.path.splitext(os.path.basename(filepath))[0] +\
            ".html"
        print("compile {filepath} to {filepath_output}".format(
            filepath        = filepath,
            filepath_output = filepath_output
        ))
        if table_of_contents:
            command = [
                "pandoc",
                "--table-of-contents",
                "--number-sections",
                "-c",
                CSS,
                filepath,
                "-o",
                filepath_output
            ]
        else:
            command = [
                "pandoc",
                "--number-sections",
                "-c",
                CSS,
                filepath,
                "-o",
                filepath_output
            ]
        process = subprocess.Popen(command, stdout = subprocess.PIPE)
        output, error = process.communicate()

def filepaths_recursive(
    directory = "."
    ):

    """
    Return a list of filepaths found recursively at the specified directory.
    """

    directory = os.path.expanduser(directory)
    filepaths = []
    for root, directories, filenames in os.walk(directory):
        for filename in filenames: 
            filepaths.append(os.path.join(root, filename))
    return filepaths

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
