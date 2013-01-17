#! /usr/bin/python
# Filename: idw_solver.py

''' '''
__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import sys
from solver import Solver

class Idw_Solver(Solver):
  
  def __init__(self, dst_point, neighbor_lst):
    self.dst_point = dst_point
    self.neighbor_lst = neighbor_lst
    self.wgt_lst = []
   
  def solve(self):
    pass
    
