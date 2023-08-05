"""ThreatConnect SDK setup.py"""
import re
import sys
from setuptools import setup, find_packages

with open('threatconnect/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__(?:\s+)?=(?:\s+)?[\'|\"]((?:[0-9]{1,3}(?:\.)?){1,3})[\'|\"]', fd.read(),
        re.MULTILINE).group(1)

# set download URL which requires a "release"
download_url = 'https://github.com/ThreatConnect-Inc/threatconnect-python/archive/{}.tar.gz'
download_url = download_url.format(version)

if not version:
    raise RuntimeError('Cannot find version information')

install_requires = [
    'python-dateutil==2.6.1',
    'pytz',
    'requests==2.18.4',
]
if sys.version_info < (3, ):
    install_requires.append('enum34')

setup(
    author='ThreatConnect (support@threatconnect.com)',
    author_email='support@threatconnect.com',
    # convert_2to3_doctests = [''],
    description='Python SDK for ThreatConnect API',
    download_url=download_url,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License'
    ],
    entry_points={
        'console_scripts': [
            'stanchion=bin.stanchion:main'
        ],
    },
    install_requires=install_requires,
    license='Apache License, Version 2',
    name='threatconnect',
    # package_dir = {'': 'src'},
    packages=find_packages(),
    url='https://github.com/ThreatConnect-Inc/threatconnect-python',
    use_2to3=True,
    use_2to3_exclude_fixers=['lib2to3.fixes.fix_print'],
    # use_2to3_fixers = [''],
    version=version
)
