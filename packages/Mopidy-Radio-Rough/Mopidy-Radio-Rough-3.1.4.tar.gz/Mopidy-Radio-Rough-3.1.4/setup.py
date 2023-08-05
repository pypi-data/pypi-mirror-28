from __future__ import unicode_literals

import re

from setuptools import find_packages, setup
from setuptools.command.install import install

def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-Radio-Rough',
    version=get_version('mopidy_radio_rough/__init__.py'),
    url='https://github.com/unusualcomputers/unusualcomputers/tree/master/code/mopidy/mopidyradiorough',
    license='Apache License, Version 2.0',
    author='Unusual Computers',
    author_email='unusual.computers@gmail.com',
    description='Rough gui for listening to internet',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 1.0',
        'Mopidy-Podcast-iTunes',
        'Mopidy-Youtube',
        'Mopidy-Rough-Base >= 3.1.4',
        'Mopidy-TuneIn',
        'Mopidy-Mixcloud',
        'Pykka >= 1.1',
        'feedparser',
        'jsonpickle',
        'mutagen',
    ],
    entry_points={
        'mopidy.ext': [
            'radio_rough = mopidy_radio_rough:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
