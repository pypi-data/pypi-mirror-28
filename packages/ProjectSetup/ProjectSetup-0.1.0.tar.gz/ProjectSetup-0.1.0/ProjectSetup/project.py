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
:mod:`__init__` -- Describe your module in one sentence

.. module:: __init__
   :platform: Unix, Windows
   :synopsis: Describe your module in one sentence
.. moduleauthor:: Micha Grandel <talk@michagrandel.de>
"""

from __future__ import unicode_literals, print_function

import subprocess
from io import open
import six
import os
import jinja2
from jinja2 import Environment, PackageLoader
from pip.operations import freeze
import shutil

try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                import cElementTree as etree
            except ImportError:
                import elementtree.ElementTree as etree

__status__ = 'development'
__author__ = 'Micha Grandel'
__version__ = ''
__copyright__ = 'written with <3 by Micha Grandel'
__license__ = 'Apache License, Version 2.0'
__contact__ = 'http://github.com/michagrandel'


class Project(object):
    """
    initialize project files
    """

    def __init__(self, name=None, path=None, **kwargs):
        """
        initialize project settings

        :param path: project path. default: current working directory
        :param name: project name. default: basename of `path`
        :param kwargs: set metadata for the project, like version, status, author, etc.
        """
        self.path = path or os.path.abspath(os.getcwd())
        self.name = name or os.path.basename(self.path)

        self.author_url = kwargs.get('url', 'https://github.com/michagrandel')
        self.author = kwargs.get('author', 'Micha Grandel')
        self.email = kwargs.get('email', 'talk@michagrandel.de')
        self.version = kwargs.get('version', '0.1.0')
        self.status = kwargs.get('status', 'planing')
        self.copyright = kwargs.get('copyright', 'Micha Grandel')
        self.year = kwargs.get('year', '2018')
        self.company = kwargs.get('company', 'Unicorn')
        self.url = 'https://github.com/michagrandel/{project}'.format(project=self.name)
        self.maintainer = kwargs.get('maintainer', self.author)
        self.maintainer_email = kwargs.get('maintainer_email', self.email)

        self.template_env = Environment(
            loader=PackageLoader(self.name),
        )
        self.templates = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../template'))
        print('Template in ' + self.templates)
        self.directories = list()

        print('Update project "{project}":\nin Project path: {path}'.format(project=self.name, path=self.path))

    def add_directory(self, name, mandatory=False):
        """
        add a directory to the project

        :param name: path of the directory inside the project path
        :param mandatory: is it optional or mandatory?
        :return: 0
        """
        if name not in [d[0] for d in self.directories]:
            fullpath = os.path.normpath(os.path.join(self.path, name))
            self.directories.append((fullpath, mandatory))
            print('"{path}" ... '.format(path=os.path.join(self.name, name)), end='')

            create_directory = mandatory or not os.path.isfile(os.path.join(self.path, 'setup.py'))
            if create_directory:
                try:
                    os.makedirs(fullpath)
                    print('Done.')
                except (OSError, IOError):
                    print('Nothing to do.')
        return 0

    def create_from_template(self, file_name, template=None):
        """
        create a file using a template

        :param file_name: name of resulting file, including path relative to project path
        :param template: filename of template file, relative to template path
        :return: 0 on success, 1 on failure
        """
        filepath = os.path.normpath(os.path.abspath(file_name.format(
            project_dir=self.path, project_name=self.name, package=self.name
        )))
        filename = os.path.basename(filepath)
        dirname = os.path.dirname(filepath)
        path = os.path.join(self.name, os.path.relpath(filepath, self.path))
        print('"{filepath}" ... '.format(filepath=path), end='')

        if not os.path.isfile(filepath):
            try:
                os.makedirs(dirname)
            except (OSError, IOError):
                pass

            if not template:
                try:
                    template = self.template_env.get_template('{0}.jinja2'.format(filename))
                except jinja2.exceptions.TemplateNotFound:
                    try:
                        template = self.template_env.get_template('{0}'.format(filename))
                    except jinja2.exceptions.TemplateNotFound:
                        print('No template "{template}.jinja2"'.format(template=filename))
                        # template = None
                        return 1

            if template:
                content = template.render(
                    project_name=self.name,
                    project_path=self.path,
                    project_url=self.author_url,
                    author=self.author,
                    author_email=self.email,
                    maintainer=self.maintainer,
                    maintainer_email=self.maintainer_email,
                    version=self.version,
                    status=self.status,
                    copyright=self.copyright,
                    company=self.company,
                    year=self.year,
                    url=self.url
                )

                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                        print('Done. Written to "{filename}"'.format(filename=filepath))
                    return 0
                except (IOError, OSError):
                    print('Could not write file.')
                    return 1
        else:
            print('Nothing to do.')
            return 0

    def generate_requirements(self):
        """ generates a requirements.txt file """
        print('"{file}" ... '.format(file=os.path.join(self.path, 'requirements.txt')), end='')
        pip_freeze = freeze.freeze()
        requirements = [requirement.replace('==', '>=') for requirement in pip_freeze]

        try:
            with open('requirements.txt', 'w', encoding='utf-8') as requirements_file:
                for requirement in requirements:
                    if self.name not in requirement:
                        requirements_file.write(requirement + '\n')
                print('Done.')
            return 0
        except (IOError, OSError):
            print('Failed.')
            return 1

    @staticmethod
    def convert(inputfile, fmt='markdown', target='rst', method='pandoc'):
        """
        convert a file

        :param inputfile: name of input file
        :param fmt: original format of input file, default: markdown
        :param target: convert to target format, default: rst
        :param method: method for conversion, currently only pandoc is supported. other methods may come in future releases
        :return:
        """
        output = '{output}.rst'.format(output=os.path.splitext(inputfile)[0])
        print('"{input}" -> "{output}" ... '.format(input=inputfile, output=output), end='')
        cmd = ['pandoc', '-f', fmt, '-t', target, inputfile, '-o', output]

        code = subprocess.call(cmd)
        if code == 0:
            print('Done.')
        else:
            print('Failed (returned {code})!'.format(code=code))

    @staticmethod
    def build(distribution='wheel', universal=True):
        """
        build project for distribution

        :param distribution: type of distribution, currently supported: wheel or source, default: wheel
        :param universal: if true and distribution is 'wheel', generate an universal wheel
        :return: return-code of setup.py
        """

        dist = {
            'wheel': 'bdist_wheel',
            'binary': 'bdist_wheel',
            'source': 'sdist'
        }.get(distribution, 'sdist')

        print('Building {universal}{dist} distribution... '.format(
            dist=distribution,
            universal='universal ' if distribution in ('wheel', 'binary') and universal else ''
        ), end='')

        try:
            command = ['python', 'setup.py', dist]
            if universal and distribution == 'wheel':
                command.append('--universal')
            code = subprocess.call(command)
        except NameError as e:
            print('{} ... '.format(e.message), end='')
            code = 1

        if code == 0:
            print('Done.')
        else:
            print('Failed (returned {code})!'.format(code=code))

        return code

    def is_idea_project(self):
        """
        check if project is a idea project, i.e. made in an IDE based on the IDEA Platform

        :return: True or False
        """
        return os.path.isdir(os.path.join(self.path, '.idea'))

    def exclude(self, paths=None):
        """
        if the project is an idea-project, you can add directories to the excluded directories

        :param paths: list of directories to be excluded, relative to the project path
        :return:
        """

        if isinstance(paths, six.string_types):
            paths = [paths]
        elif not paths:
            paths = []

        pattern = 'file://$MODULE_DIR$/{folder}'

        # want to exclude these folders:
        exclude_folders = ['venv', 'dist', 'build', 'docs/build']

        path = ''
        for path in paths:
            if path not in exclude_folders:
                exclude_folders.append(path)

        if not self.is_idea_project():
            raise RuntimeError('Excluding folders is only implemented for IDEA Projects.')

        if not os.path.isdir(os.path.join(self.path, path)):
            raise RuntimeError('"{}" not found.'.format(path))

        project_file = os.path.join(self.path, '.idea', '{}.iml'.format(self.name))

        # create a backup of the file
        backup_file = os.path.join(self.path, '.idea', '{}.backup.iml'.format(self.name))
        shutil.copy2(project_file, backup_file)

        reader = etree.parse(project_file)
        root = reader.getroot()

        # already excluded:
        excluded_folders = [folder.attrib['url'] for folder in root.iter('excludeFolder')]

        # for folder in exclude_folders:
        #     folder_url = pattern.format(folder=folder)
        #     if folder_url:

        for excluded_folder in root.iter('excludeFolder'):
            excluded_folders.append(excluded_folder.attrib['url'])

        # remove folders from list that are already excluded
        for path in exclude_folders:
            if pattern.format(folder=path) in excluded_folders:
                exclude_folders.pop(exclude_folders.index(path))

        # get content element
        content_element = []
        for child in root:
            if child.find('content') is not None:
                content_element = child.find('content')
                break

        if len(content_element):
            # append new excluded folders
            for folder in exclude_folders:
                # exclude_folder_element.attrib['url'] = pattern.format(folder=folder)
                new_element = etree.SubElement(content_element, 'excludeFolder')
                new_element.attrib['url'] = pattern.format(folder=folder)
                content_element.append(new_element)

            hook = content_element.getparent()
            hook.remove(content_element)
            hook.append(content_element)

        # write to file
        # writer = etree.ElementTree(root)

        with open(project_file, 'wb') as output_file:
            output_file.write(etree.tostring(root, pretty_print=True))
