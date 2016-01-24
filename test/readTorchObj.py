#!/usr/bin/env python

from pprint import pprint

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))

import torchio

#----------------------------------------------------------------------
# main
#----------------------------------------------------------------------

import sys

ARGV = sys.argv[1:]

assert len(ARGV) == 1, "must specify exactly one command line argument (torch input file)"

fname = ARGV.pop(0)
fin = open(fname)

infile = torchio.InputFile(fin, mode = 'binary')

obj = infile.readObject()

remainder = fin.read()

assert len(remainder) == 0, "%d bytes unread" % len(remainder)
