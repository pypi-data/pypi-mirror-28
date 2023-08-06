from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import os
from six.moves import configparser

from eph.config import get_config_file, create_config_file

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

parser = configparser.ConfigParser()
parser.read('setup.cfg')
meta = dict(parser.items('metadata'))


def install_config():
    config_file = get_config_file()
    if not os.path.isfile(config_file):
        create_config_file(config_file)


class CustomInstall(install):

    def run(self):
        install_config()
        install.run(self)


class CustomDevelop(develop):

    def run(self):
        install_config()
        develop.run(self)


setup(
    name=meta['package'],
    version=meta['release'],
    description=meta['description'],
    long_description=long_description,
    author=meta['author'],
    author_email=meta['author_email'],
    license=meta['license'],
    url=meta['url'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    install_requires=[
        'setuptools',
		'six',
        'requests',
        'astropy',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'eph=eph.cli:main',
        ],
    },
    cmdclass={
        'develop': CustomDevelop,
        'install': CustomInstall,
    },
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],
)
