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
#                     written with <3 by Micha Grandel, talk@michagrandel.de
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

"""ProjectSetup - describe your project

A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from __future__ import unicode_literals, print_function
# To use a consistent encoding
from io import open
import os

# Always prefer setuptools over distutils
try:
    from setuptools import setup, find_packages

    packages = find_packages(exclude=['contrib', 'docs', 'tests'])
except ImportError:
    from distutils.core import setup
    from pkgutil import walk_packages

    import ProjectSetup


    def find_packages(path=__path__, prefix=""):
        """
        replacement for setuptools find_packages

        :param path:
        :param prefix:

        :return:
        """
        yield prefix
        prefix = prefix + "."
        for _, name, ispkg in walk_packages(path, prefix):
            if ispkg:
                yield name


    packages = list(find_packages(ProjectSetup.__path__, ProjectSetup.__name__))

__status__ = 'planing'
__author__ = 'Micha Grandel'
__maintainer__ = 'Micha Grandel'
__version__ = '0.1.0'
__copyright__ = 'written with <3 by Micha Grandel'
__license__ = 'Apache 2.0 license'
__contact__ = 'talk@michagrandel.de'
__maintainer_contact__ = 'talk@michagrandel.de'

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'Readme.rst'), encoding='utf-8') as f:
    long_description = f.read()


def requirements(category='install'):
    """
    return list with requirements

    :param category: category of requirements
    :return: list with requirements
    """
    if category.lower().startswith('install'):
        file_ = 'requirements.txt'
    elif category.lower().startswith('dev'):
        file_ = 'development-requirements.txt'
    elif category.lower().startswith('test'):
        file_ = 'test-requirements.txt'
    else:
        return []

    try:
        with open(file_, 'r', encoding='utf-8') as requirements_file:
            content = requirements_file.read()
        content = content.split('\n')
    except (IOError, OSError) as error:
        content = []

    return content


# DATA
setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    name='ProjectSetup',  # Required

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,  # Required

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='describe your project',  # Required

    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional

    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url='https://github.com/michagrandel/ProjectSetup',  # Optional

    # This should be your name or the name of the organization which owns the
    # project.
    author=__author__,  # Optional

    # This should be a valid email address corresponding to the author listed
    # above.
    author_email=__contact__,  # Optional

    # maintainer info
    maintainer=__maintainer__,  # Optional
    maintainer_email=__maintainer_contact__,  # Optional

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Optional
        # How mature is this project? Common values are
        # Valid Values:
        #
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',

        # Indicate who your project is intended for
        # Valid Values:
        #
        # 'Intended Audience :: Customer Service',
        # 'Intended Audience :: Developers',
        # 'Intended Audience :: Education',
        # 'Intended Audience :: End Users/Desktop',
        # 'Intended Audience :: Financial and Insurance Industry',
        # 'Intended Audience :: Healthcare Industry',
        # 'Intended Audience :: Information Technology',
        # 'Intended Audience :: Legal Industry',
        # 'Intended Audience :: Manufacturing',
        # 'Intended Audience :: Other Audience',
        # 'Intended Audience :: Religion',
        # 'Intended Audience :: Science/Research',
        # 'Intended Audience :: System Administrators',
        # 'Intended Audience :: Telecommunications Industry',

        # Valid Values:
        #
        # 'Topic :: Artistic Software',
        # 'Topic :: Communications',
        # 'Topic :: Communications :: Chat',
        # 'Topic :: Communications :: Chat :: Internet Relay Chat',
        # 'Topic :: Communications :: Email',
        # 'Topic :: Communications :: Email :: Address Book',
        # 'Topic :: Communications :: Email :: Email Clients (MUA)',
        # 'Topic :: Communications :: Email :: Filters',
        # 'Topic :: Communications :: Email :: Mailing List Servers',
        # 'Topic :: Communications :: Email :: Mail Transport Agents',
        # 'Topic :: Database',
        # 'Topic :: Desktop Environment',
        # 'Topic :: Desktop Environment :: File Managers',
        # 'Topic :: Desktop Environment :: Gnome',
        # 'Topic :: Desktop Environment :: Screen Savers',
        # 'Topic :: Documentation',
        # 'Topic :: Documentation :: Sphinx',
        # 'Topic :: Education',
        # 'Topic :: Education :: Testing',
        # 'Topic :: Games/Entertainment',
        # 'Topic :: Games/Entertainment :: Arcade',
        # 'Topic :: Games/Entertainment :: Board Games',
        # 'Topic :: Games/Entertainment :: First Person Shooters',
        # 'Topic :: Games/Entertainment :: Fortune Cookies',
        # 'Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)',
        # 'Topic :: Games/Entertainment :: Puzzle Games',
        # 'Topic :: Games/Entertainment :: Real Time Strategy',
        # 'Topic :: Games/Entertainment :: Role-Playing',
        # 'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
        # 'Topic :: Games/Entertainment :: Simulation',
        # 'Topic :: Games/Entertainment :: Turn Based Strategy',
        # 'Topic :: Internet',
        # 'Topic :: Internet :: WWW/HTTP',
        # 'Topic :: Internet :: WWW/HTTP :: Browsers',
        # 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        # 'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        # 'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',
        # 'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki',
        # 'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        # 'Topic :: Internet :: WWW/HTTP :: Site Management',
        # 'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
        # 'Topic :: Internet :: WWW/HTTP :: WSGI',
        # 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        # 'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        # 'Topic :: Multimedia',
        # 'Topic :: Multimedia :: Graphics',
        # 'Topic :: Multimedia :: Graphics :: 3D Modeling',
        # 'Topic :: Multimedia :: Graphics :: 3D Rendering',
        # 'Topic :: Multimedia :: Graphics :: Capture',
        # 'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        # 'Topic :: Multimedia :: Graphics :: Capture :: Scanners',
        # 'Topic :: Multimedia :: Graphics :: Capture :: Screen Capture',
        # 'Topic :: Multimedia :: Graphics :: Editors',
        # 'Topic :: Multimedia :: Graphics :: Editors :: Raster-Based',
        # 'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
        # 'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        # 'Topic :: Multimedia :: Graphics :: Presentation',
        # 'Topic :: Multimedia :: Graphics :: Viewers',
        # 'Topic :: Multimedia :: Sound/Audio',
        # 'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
        # 'Topic :: Multimedia :: Sound/Audio :: Conversion',
        # 'Topic :: Multimedia :: Sound/Audio :: Speech',
        # 'Topic :: Multimedia :: Video',
        # 'Topic :: Multimedia :: Video :: Capture',
        # 'Topic :: Multimedia :: Video :: Conversion',
        # 'Topic :: Multimedia :: Video :: Display',
        # 'Topic :: Multimedia :: Video :: Non-Linear Editor',
        # 'Topic :: Office/Business',
        # 'Topic :: Office/Business :: Financial :: Spreadsheet',
        # 'Topic :: Office/Business :: Office Suites',
        # 'Topic :: Other/Nonlisted Topic',
        # 'Topic :: Printing',
        # 'Topic :: Religion',
        # 'Topic :: Scientific/Engineering',
        # 'Topic :: Scientific/Engineering :: Artificial Intelligence',
        # 'Topic :: Scientific/Engineering :: Artificial Life',
        # 'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        # 'Topic :: Scientific/Engineering :: Image Recognition',
        # 'Topic :: Scientific/Engineering :: Visualization',
        # 'Topic :: Security',
        # 'Topic :: Security :: Cryptography',
        # 'Topic :: Software Development :: Interpreters',
        # 'Topic :: Software Development :: Libraries :: Python Modules',
        # 'Topic :: Software Development :: User Interfaces',
        # 'Topic :: Software Development :: Version Control :: Git',
        # 'Topic :: Software Development :: Widget Sets',
        # 'Topic :: System',
        # 'Topic :: System :: Archiving',
        # 'Topic :: System :: Archiving :: Backup',
        # 'Topic :: System :: Archiving :: Compression',
        # 'Topic :: System :: Archiving :: Mirroring',
        # 'Topic :: System :: Archiving :: Packaging',
        # 'Topic :: System :: Installation/Setup',
        # 'Topic :: System :: Logging',
        # 'Topic :: System :: Monitoring',
        # 'Topic :: System :: Networking',
        # 'Topic :: System :: Software Distribution',
        # 'Topic :: System :: Systems Administration',
        # 'Topic :: System :: System Shells',
        # 'Topic :: Terminals',
        # 'Topic :: Text Editors',
        # 'Topic :: Text Editors :: Integrated Development Environments (IDE)',
        # 'Topic :: Text Processing',
        # 'Topic :: Text Processing :: Markup',
        # 'Topic :: Text Processing :: Markup :: HTML',
        # 'Topic :: Text Processing :: Markup :: LaTeX',
        # 'Topic :: Text Processing :: Markup :: XML',
        # 'Topic :: Utilities',

        # Pick your license as you wish
        #
        # Valid Values:
        #
        # 'License :: Free For Educational Use',
        # 'License :: Free For Home Use',
        # 'License :: Free for non-commercial use',
        # 'License :: Freely Distributable',
        # 'License :: Free To Use But Restricted',
        # 'License :: Freeware',
        # 'License :: OSI Approved',
        'License :: OSI Approved :: Apache Software License',
        # 'License :: OSI Approved :: BSD License',
        # 'License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)',
        # 'License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)',
        # 'License :: OSI Approved :: GNU Affero General Public License v3',
        # 'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        # 'License :: OSI Approved :: GNU Free Documentation License (FDL)',
        # 'License :: OSI Approved :: GNU General Public License (GPL)',
        # 'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        # 'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        # 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        # 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        # 'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        # 'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        # 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        # 'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        # 'License :: OSI Approved :: MIT License',
        # 'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        # 'License :: OSI Approved :: Python Software Foundation License',
        # 'License :: OSI Approved :: Qt Public License (QPL)',

        # 'License :: Other/Proprietary License',
        #
        # Valid Values:
        #
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.3',
        # 'Programming Language :: Python :: 2.4',
        # 'Programming Language :: Python :: 2.5',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.0',
        # 'Programming Language :: Python :: 3.1',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: 3 :: Only',

        # Specify the Operating System on which your software runs
        #
        # Valid Values:
        #
        # 'Operating System :: Android',
        # 'Operating System :: iOS',
        # 'Operating System :: MacOS',
        # 'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        # 'Operating System :: Microsoft :: MS-DOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: OS Independent',
        # 'Operating System :: Other OS',
        # 'Operating System :: POSIX',
        # 'Operating System :: POSIX :: BSD',
        # 'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        # 'Operating System :: POSIX :: Other',

        # Specify the language of your application
        #
        # Valid Values:
        #
        # 'Natural Language :: Afrikaans',
        # 'Natural Language :: Arabic',
        # 'Natural Language :: Bengali',
        # 'Natural Language :: Bosnian',
        # 'Natural Language :: Bulgarian',
        # 'Natural Language :: Cantonese',
        # 'Natural Language :: Catalan',
        # 'Natural Language :: Chinese (Simplified)',
        # 'Natural Language :: Chinese (Traditional)',
        # 'Natural Language :: Croatian',
        # 'Natural Language :: Czech',
        # 'Natural Language :: Danish',
        # 'Natural Language :: Dutch',
        'Natural Language :: English',
        # 'Natural Language :: Esperanto',
        # 'Natural Language :: Finnish',
        # 'Natural Language :: French',
        # 'Natural Language :: Galician',
        # 'Natural Language :: German',
        # 'Natural Language :: Greek',
        # 'Natural Language :: Hebrew',
        # 'Natural Language :: Hindi',
        # 'Natural Language :: Hungarian',
        # 'Natural Language :: Icelandic',
        # 'Natural Language :: Indonesian',
        # 'Natural Language :: Italian',
        # 'Natural Language :: Japanese',
        # 'Natural Language :: Javanese',
        # 'Natural Language :: Korean',
        # 'Natural Language :: Latin',
        # 'Natural Language :: Latvian',
        # 'Natural Language :: Macedonian',
        # 'Natural Language :: Malay',
        # 'Natural Language :: Marathi',
        # 'Natural Language :: Norwegian',
        # 'Natural Language :: Panjabi',
        # 'Natural Language :: Persian',
        # 'Natural Language :: Polish',
        # 'Natural Language :: Portuguese',
        # 'Natural Language :: Portuguese (Brazilian)',
        # 'Natural Language :: Romanian',
        # 'Natural Language :: Russian',
        # 'Natural Language :: Serbian',
        # 'Natural Language :: Slovak',
        # 'Natural Language :: Slovenian',
        # 'Natural Language :: Spanish',
        # 'Natural Language :: Swedish',
        # 'Natural Language :: Tamil',
        # 'Natural Language :: Telugu',
        # 'Natural Language :: Thai',
        # 'Natural Language :: Turkish',
        # 'Natural Language :: Ukranian',
        # 'Natural Language :: Urdu',
        # 'Natural Language :: Vietnamese',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='python',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=packages,  # Required

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=requirements(),  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional
        'dev': requirements('dev'),
        'test': requirements('test'),
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    #
    # package_data = {  # Optional
    #     'Backup': ['templates/*.html'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #
    # sys.prefix:
    # A string giving the site-specific directory prefix where the platform independent
    # Python files are installed; by default, this is the string '/usr/local'.
    # This can be set at build time with the --prefix argument to the configure script.
    # The main collection of Python library modules is installed in the directory prefix/lib/pythonX.Y
    # while the platform independent header files (all except pyconfig.h) are stored in prefix/include/pythonX.Y,
    # where X.Y is the version number of Python, for example 2.7.
    #
    # data_files = [
    #     ('Backup API/0.1.0/openapi',
    #      [
    #         'openapi/v0.1.0/openapi.html',
    #         'openapi/v0.1.0/openapi.json',
    #         'openapi/v0.1.0/openapi.yaml',
    #      ]),
    #     ('Backup API/0.1.0/templates',
    #      [
    #         'templates/openapi.html'
    #      ])
    # ],  # Optional
    #
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    #
    # entry_points = {  # Optional
    #    'console_scripts': [
    #        'sample=script.py:main',
    #    ],
    # },
    scripts=[os.path.join('script', f) for f in os.listdir('script')]
)