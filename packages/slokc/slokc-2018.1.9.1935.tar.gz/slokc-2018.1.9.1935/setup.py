#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "slokc",
        version          = "2018.01.09.1935",
        description      = "Kelvin Building automated Wi-Fi login program",
        long_description = long_description(),
        url              = "https://github.com/wdbm/suck_lord_kelvin_cock",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "suck_lord_kelvin_cock"
                           ],
        install_requires = [
                           "docopt"
                           ],
        scripts          = [
                           "suck_lord_kelvin_cock.py"
                           ],
        entry_points     = """
                           [console_scripts]
                           suck_lord_kelvin_cock = suck_lord_kelvin_cock:suck_lord_kelvin_cock
                           """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
