#!/usr/bin/env python
from setuptools import setup, find_packages


REPO_NAME = 'chickenzord/btcid-py'
VERSION = '0.1.0'
ARCHIVE_URL = 'https://github.com/%s/archive/v%s.tar.gz' % (REPO_NAME, VERSION)

setup(
    # packaging
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={},
    data_files=[('', ['LICENSE.txt'])],
    install_requires=[
        'requests',
        'future',
    ],
    setup_requires=[
        'flake8',
    ],
    tests_require=[
    ],
    entry_points={
    },
    zip_safe=False,

    # metadata
    name='btcid',
    version=VERSION,
    author='Akhyar Amarullah',
    author_email='akhyrul@gmail.com',
    description='Python wrapper for bitcoin.co.id API',
    long_description=open('README.rst').read(),
    download_url=ARCHIVE_URL,
    license='MIT',
    keywords=['cryptocurrency', 'bitcoin', 'indonesia'],
    url='https://github.com/%s' % (REPO_NAME),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ],
)
