#! /usr/bin/python
# Filename: collineation.py

''' '''

__author__ = ['Wu Hong<xunzhangthU@gmail.com>']

def check_collineation(p1, p2, p3):
  if (p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0]):
    return False 
  else:
    return True
