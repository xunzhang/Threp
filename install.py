#! /usr/bin/python
# Filename: install.py

import os
import sys
from threp.config.threp_dir import THREP_DIR

# check THREP_DIR
if not THREP_DIR:
  print 'Please modify var THREP_DIR at ./threp/config/threp_dir.py file.'
  print 'THREP_DIR needs to be set up with the top Threp directory.'
  exit(1)

# cp import file for modules
filename = 'threp_dir.py'

command = 'cp ./threp/config/' + filename + ' ./threp/interp/' + filename
os.system(command)
command = 'cp ./threp/config/' + filename + ' ./threp/interp/algs/' + filename
os.system(command)
command = 'cp ./threp/config/' + filename + ' ./threp/search/' + filename
os.system(command)
command = 'cp ./threp/config/' + filename + ' ./threp/solver/' + filename
os.system(command)

