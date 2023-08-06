#!/usr/bin/env python

import os

def _path_to_file(pfile):
    import timemory
    return '{}/timemory-supp/{}'.format(os.path.dirname(timemory.__file__), pfile)

def mpi_exe_info():
    print (open(_path_to_file('mpi_exe_info.txt'), 'r').read())

def mpi_c_info():
    print (open(_path_to_file('mpi_c_info.txt'), 'r').read())

def mpi_cxx_info():
    print (open(_path_to_file('mpi_cxx_info.txt'), 'r').read())

