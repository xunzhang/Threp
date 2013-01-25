#! /usr/bin/python
# Filename: install.py

import os
import sys
from config.threp_dir import THREP_DIR

# check THREP_DIR
if not THREP_DIR:
  print 'Please modify var THREP_DIR at ./config/threp_dir.py file.'
  print 'THREP_DIR needs to be set up with the top Threp directory.'
  exit(1)

# cp import file for modules
filename = 'threp_dir.py'

command = 'cp ./config/' + filename + ' ./interp/' + filename
os.system(command)
command = 'cp ./config/' + filename + ' ./interp/algs' + filename
os.system(command)
command = 'cp ./config/' + filename + ' ./search/' + filename
os.system(command)
command = 'cp ./config/' + filename + ' ./solver' + filename
os.system(command)

