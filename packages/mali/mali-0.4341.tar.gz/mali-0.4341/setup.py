# -*- coding: utf8 -*-
import os

import setuptools
from setuptools import setup, find_packages
import setuptools.command.bdist_egg

build = os.environ.get('PIP_BUILD', 100)
keywords = os.environ.get('PIP_KEYWORDS', 'test')


version = '0.{}'.format(build)

with open('requirements.txt') as f:
    install_requires = [r for r in f.readlines() if len(r.strip()) > 0]


class BuildPyCommand(setuptools.command.bdist_egg.bdist_egg):
  """Custom build command."""

  def run(self):
    print('Doing rc install')
    setuptools.command.bdist_egg.bdist_egg.run(self)


setup(
    name='mali',
    version=version,
    description='Command line tool for missinglink.ai platform',
    author='missinglink.ai',
    author_email='support+mali@missinglink.ai',
    url='https://missinglink.ai',
    license='Apache',
    py_modules=['mali'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(),
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        mali=mali:main
    ''',
)
