#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import tox
        errno = tox.cmdline()
        sys.exit(errno)


setup(
    name='sphinxcontrib-images',
    version='0.9.2',
    url='https://github.com/sphinx-contrib/images',
    download_url='https://pypi.python.org/pypi/sphinxcontrib-images',
    project_urls={
        'Bug Tracker': 'https://github.com/sphinx-contrib/images/issues',
        'Documentation': 'https://sphinxcontrib-images.readthedocs.io/',
    },
    license='Apache 2',
    author=u'Tomasz Czyż',
    author_email='tomasz.czyz@gmail.com',
    description='Sphinx extension for thumbnails',
    long_description=codecs.open('README.rst', encoding="utf8").read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Documentation',
    ],
    entry_points={
        'console_scripts':[
            'sphinxcontrib-images=sphinxcontrib.images:main',
        ],
        'sphinxcontrib.images.backend':[
            'LightBox2 = sphinxcontrib_images_lightbox2:LightBox2',
            'FakeBackend = sphinxcontrib_images_lightbox2:LightBox2',
        ]
    },
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['wheel'],
    install_requires=['sphinx>=1.8.5,<2.0;python_version<"3.0"',
                      'sphinx>=2.0;python_version>="3.0"',
                      'requests>2.2,<3'],
    tests_require=['tox==3.2.1'],
    cmdclass = {'test': Tox},
    namespace_packages=['sphinxcontrib'],
)
