#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

requires = [
]

def main():
    description = 'mbglob is a wrapper libs for glob.glob.'

    setup(
        name='mbglob',
        version='0.0.3',
        author='nabeen',
        author_email='watanabe_kenichiro@hasigo.co.jp',
        url='https://github.com/nabeen/mbglob',
        description=description,
        long_description=description,
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(),
        install_requires=requires,
        tests_require=[],
        setup_requires=[],
    )


if __name__ == '__main__':
    main()
