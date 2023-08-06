#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @formatter:off
#
#                                             ,,
#                                             db
#     \
#     _\,,          `7MM  `7MM  `7MMpMMMb.  `7MM  ,p6"bo   ,pW"Wq.`7Mb,od8 `7MMpMMMb.
#    "-=\~     _      MM    MM    MM    MM    MM 6M'  OO  6W'   `Wb MM' "'   MM    MM
#       \\~___( ~     MM    MM    MM    MM    MM 8M       8M     M8 MM       MM    MM
#      _|/---\\_      MM    MM    MM    MM    MM 8M       8M     M8 MM       MM    MM
#     \        \      MM    MM    MM    MM    MM YM.    , YA.   ,A9 MM       MM    MM
#                     `Mbod"YML..JMML  JMML..JMML.YMbmd'   `Ybmd9'.JMML.   .JMML  JMML.
#
#                     written with <3 by Micha Grandel, talk@michagrandel.com
#                     
#                     Project:         https://github.com/michagrandel/ProjectSetup
#                     Report a bug:    https://github.com/michagrandel/ProjectSetup/issues
#                     Contribute:      https://github.com/michagrandel/ProjectSetup/wiki/Contribute
#                     
#                     Facebook:        https://me.me/micha.animator
#                     Instagram:       @michagrandel
#                     -----------------------------------------------------------------
#                     
#                     Copyright 2018 Micha Grandel
#
#                     Licensed under the Apache License, Version 2.0 (the 'License');
#                     you may not use this file except in compliance with the License.
#                     You may obtain a copy of the License at
#                     
#                     http://www.apache.org/licenses/LICENSE-2.0
#                     
#                     Unless required by applicable law or agreed to in writing,
#                     software distributed under the License is distributed on an
#                     'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
#                     either express or implied. See the License for the specific
#                     language governing permissions and limitations under the License.
#                     -----------------------------------------------------------------
#                     @formatter:on

"""
:mod:`init_project` -- Describe your module in one sentence

.. module:: init_project
   :platform: Unix, Windows
   :synopsis: Describe your module in one sentence
.. moduleauthor:: Micha Grandel <talk@michagrandel.de>
"""


from __future__ import unicode_literals, print_function

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../..')))

from ProjectSetup import *

__status__ = 'development'
__author__ = 'Micha Grandel'
__version__ = '0.1.1'
__copyright__ = 'written with <3 by Micha Grandel'
__license__ = 'Apache License, Version 2.0'
__contact__ = 'http://github.com/michagrandel'


if __name__ == '__main__':

    project = Project()
    directories = {
        'mandatory': {
            project.name,
            'test',
            'docs',
            'docs/source',
            'docs/source/_static',
            'docs/source/_templates',
            'docs/source',
        },
        'optional': {
            'script'
        }
    }
    files = [
        "{package}/__init__.py",
        "docs/issue_template.md",
        "docs/PULL_REQUEST_TEMPLATE.md",
        "script/discover.py",
        ".travis.yml",
        "CODE_OF_CONDUCT.md",
        "Contributing.md",
        "How_to_install_Python_2.7.md",
        "LICENSE",
        "Readme.md",
        "requirements.txt",
        "setup.py",
        "docs/source/conf.py",
        "docs/source/index.rst",
        "docs/make.bat",
        "docs/Makefile"
    ]

    # create directories and files
    [project.add_directory(path, True) for path in directories['mandatory']]
    [project.add_directory(path) for path in directories['optional']]
    map(project.create_from_template, files)

    # generate requirements.txt and Readme.rst (for PyPI)
    project.generate_requirements()
    Project.convert('Readme.md')

    # build project
    Project.build('source')
    Project.build()

    project.exclude(['dist', 'docs/build', 'build'])
