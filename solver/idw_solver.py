#! /usr/bin/python
# Filename: idw_solver.py

''' '''
__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import sys
from solver import Solver
from distance import euc_dist

class Idw_Solver(Solver):
  
  def __init__(self, dst_point, neighbor_lst, eps, power):
    self.dst_point = dst_point
    self.neighbor_lst = neighbor_lst
    self.wgt_lst = []
    self.eps = eps
    self.power = power
   
  def solve(self):
    wgt_sum = 0
    for pnt in self.neighbor_lst:
      dist = euc_dist(self.dst_point, pnt)
      val = 1 / (dist + self.eps) **self.power
      self.wgt_lst.append(val)
      wgt_sum +=  val
    # normalization
    for i in range(len(self.wgt_lst)):
      self.wgt_lst[i] /= wgt_sum
    
