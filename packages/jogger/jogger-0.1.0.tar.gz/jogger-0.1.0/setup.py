#!/usr/bin/env python
import textwrap
from setuptools import setup, find_packages

__version__ = '0.1.0'

long_description = textwrap.dedent('''\
    Jogger is a tool to add advanced logging possibilities to your code.
    Add handlers as your code become bigger without changing everything.''')

setup(
    name='jogger',
    version=__version__,
    description='Simple tool for an advanced logging experience',
    long_description=long_description,
    author='Noel Martignoni',
    author_email='noel@martignoni.fr',
    url='https://gitlab.com/xneomac/jogger',
    install_requires=['future', 'logstash'],
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Logging',
        'Topic :: Utilities']
)
