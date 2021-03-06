#! /usr/bin/python
# Filename: solver.py

''' '''

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import math
import sys

class Solver(Exception):
  
  def __init__(self, dst_point, neighbor_lst):
    self.dst_point = dst_point
    self.neighbor_lst = neighbor_lst
    self.wgt_lst = []
  
  def __check_delta(self, delta):
    if delta < 0:
      return False
    else:
      return True
     
  # solveing quadratics with a * x^2 + b * x + c = 0
  def solve_quadratics(self, a, b ,c):
    delta = b * b - 4 * a * c
    if not self.__check_delta(delta):
      print 'Error in solving a quadratics. There must be not imaginary root in Threp.'
      sys.exit()
    delta = math.sqrt(delta)
    down = 2 * a
    r1 = (-b + delta) / down
    r2 = (-b - delta) / down
    return r1, r2

  def select_legal_root(self, root1, root2):
    r = 0.0
    if root1 >= -1e-10 and root1 <= 1.0:
      print 'root1 is legal.'
      r = root1
    if root2 >= -1e-10 and root2 <= 1.0:
      print 'root2 is legal.'
      r = root2
    print root1
    print root2
    return r  

