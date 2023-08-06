#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools
import pypandoc

def main():

    setuptools.setup(
        name             = "supermodule",
        version          = "2018.01.21.0158",
        description      = "super utilities",
        long_description = "things",
        url              = "https://github.com/wdbm/junk",
        author           = "John Drake",
        author_email     = "j.drake@sern.ch",
        license          = "GPLv3",
        packages         = [
                           "supermodule"
                           ]
    )

if __name__ == "__main__":
    main()
