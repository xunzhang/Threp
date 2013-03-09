#! /usr/bin/python
# Filename: pole_solver.py

''' '''

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import sys
from solver import Solver
from distance import sph_dist

class Pole_Solver(Solver):
  
  def __init__(self, dst_point, pole_pnts, n):
    Solver.__init__(self, dst_point, pole_pnts)
    self.num = n
    
  def solve(self):
    if self.num > 10:
      print 'Pole interp error!'
      print 'Now, Threp use 10 as max pole interp points.'
      sys.exit()
    #for i in xrange(self.num):
    #  self.wgt_lst.append(1.0/self.num)
    wgt_sum = 0
    for pnt in self.neighbor_lst[0:self.num]:
      dist = sph_dist(self.dst_point, pnt)
      val = 1.0 / (dist + 1.0e-6) **2
      self.wgt_lst.append(val)
      wgt_sum += val
    # normalization
    for i in range(len(self.wgt_lst)):
      self.wgt_lst[i] /= wgt_sum
