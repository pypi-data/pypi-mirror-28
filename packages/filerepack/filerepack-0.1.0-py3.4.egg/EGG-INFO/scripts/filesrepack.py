#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys, os ,random

from os.path import isfile, join, exists, abspath
from shutil import move, rmtree
from os import listdir, walk
import uuid
import logging
from filerepack import FileRepacker

if __name__ == "__main__":
    dr = FileRepacker()
    import pprint
    pprint.pprint(dr.repack_zip_file(sys.argv[1]))
