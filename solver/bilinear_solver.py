#! /usr/bin/python
# Filename: bilinear_solver.py

''' '''
__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import sys
from solver import Solver

class Bilinear_Solver(Solver):
  
  # Suppose the vertex rect list is sorted by:
  # 1---3      w1---w3
  # |   |  ->   |   |    ->  wgt_lst = [w0, w1, w2, w3]
  # 0---2      w0---w2
  # Suppose the vertex rect list is sorted by:
  # 1---2      w1---w2
  # |   |  ->   |   |    ->  wgt_lst = [w0, w1, w2, w3]
  # 0---3      w0---w3
  def __init__(self, dst_point, vertex_rect):
    Solver.__init__(self, dst_point, vertex_rect)
    self.vertex_rect = self.neighbor_lst
    # init wgt_lst as [0.0, 0.0, 0.0, 0.0]
    self.wgt_lst.append(0.0)
    self.wgt_lst.append(0.0)
    self.wgt_lst.append(0.0)
    self.wgt_lst.append(0.0)
    
  def regular_solve(self):
    # check x-dim regular
    if self.vertex_rect[0][0] != self.vertex_rect[1][0] and self.vertex_rect[2][0] != self.vertex_rect[3][0]:
      print 'X coord is not the same. Not regular box!'
      #sys.exit()
    # check y-dim regular
    if self.vertex_rect[0][1] != self.vertex_rect[3][1] and self.vertex_rect[1][1] != self.vertex_rect[2][1]:
      print 'Y coord is not the same. Not regular box!'
      #sys.exit()

    alpha = (self.dst_point[0] - self.vertex_rect[0][0]) / (self.vertex_rect[3][0] - self.vertex_rect[0][0])
    beta = (self.dst_point[1] - self.vertex_rect[0][1]) / (self.vertex_rect[1][1] - self.vertex_rect[0][1])

    self.wgt_lst[0] = (1 - alpha) * (1 - beta)
    self.wgt_lst[1] = (1 - alpha) * beta
    self.wgt_lst[2] = alpha * beta
    self.wgt_lst[3] = alpha * (1 - beta)
    print self.wgt_lst

