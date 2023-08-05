#!C:\Python36\python.EXE
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
    results = dr.repack_zip_file(sys.argv[1])
    print('File %s shrinked %d -> %d (%f%%)' % (sys.argv[1].encode('utf8'), results['final'][0], results['final'][1], results['final'][2]))
    if len(results['files']) > 0:
        print('Files recompressed:')
        for fdata in results['files']:
            print('- %s: %d -> %d (%f%%)' % (fdata[0], fdata[1], fdata[2], fdata[3]))
