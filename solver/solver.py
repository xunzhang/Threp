#! /usr/bin/python
# Filename: solver.py

''' '''

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

class Solver(Exception):
  
  def __init__(self, dst_point, neighbor_lst):
    self.dst_point = dst_point
    self.neighbor_lst = neighbor_lst
    self.wgt_lst = []
