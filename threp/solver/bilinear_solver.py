#! /usr/bin/python
# Filename: bilinear_solver.py

''' '''
__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import sys
from solver import Solver

class Bilinear_Solver(Solver):
  
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
    
  #         1---2
  # solve  /     \  or other normal case
  #       0-------3
  def solve_bilinear_case1(self):
    print 'I am in case1.'
    x34 = self.vertex_rect[2][0] - self.vertex_rect[3][0]
    y34 = self.vertex_rect[2][1] - self.vertex_rect[3][1]
    x21 = self.vertex_rect[1][0] - self.vertex_rect[0][0]
    y21 = self.vertex_rect[1][1] - self.vertex_rect[0][1]
    x41 = self.vertex_rect[3][0] - self.vertex_rect[0][0]
    y41 = self.vertex_rect[3][1] - self.vertex_rect[0][1]

    a = x34 * y21 - x21 * y34
    b = self.dst_point[0] * (y34 - y21) + self.dst_point[1] * (x21 - x34) + y34 * self.vertex_rect[0][0] - x34 * self.vertex_rect[0][1] + self.vertex_rect[3][0] * y21 - self.vertex_rect[3][1] * x21
    c = self.dst_point[0] * y41 - self.dst_point[1] * x41 + self.vertex_rect[3][0] * self.vertex_rect[0][1] - self.vertex_rect[0][0] * self.vertex_rect[3][1]
    
    t1, t2 = Solver.solve_quadratics(self, a, b, c)
    t = Solver.check_legal_root(t1, t2)
    s = (self.dst_point[0] - self.vertex_rect[0][0] - x21 * t) / (self.vertex_rect[3][0] + x34 * t - self.vertex_rect[0][0] - x21 * t)
    self.wgt_lst[0] = (1 - s) * (1 - t)
    self.wgt_lst[1] = (1 - s) * t
    self.wgt_lst[2] = s * t
    self.wgt_lst[3] = s * (1 - t)

  def solve_bilinear_case2(self):
    print 'I am in case2.'
    x32 = self.vertex_rect[2][0] - self.vertex_rect[1][0]
    y32 = self.vertex_rect[2][1] - self.vertex_rect[1][1]
    x41 = self.vertex_rect[3][0] - self.vertex_rect[0][0]
    y41 = self.vertex_rect[3][1] - self.vertex_rect[0][1]
    x21 = self.vertex_rect[1][0] - self.vertex_rect[0][0]
    y21 = self.vertex_rect[1][1] - self.vertex_rect[0][1]
    a = x32 * y41 - x41 * y32
    b = self.dst_point[0] * (y32 - y41) + self.dst_point[1] * (x41 - x32) + self.vertex_rect[0][1] * x32 - self.vertex_rect[0][0] * y32 + self.vertex_rect[1][0] * y41 - self.vertex_rect[1][1]* x41
    c = self.dst_point[0] * y21 - self.dst_point[1] * x21 + self.vertex_rect[1][0] * self.vertex_rect[0][1] - self.vertex_rect[0][0] * self.vertex_rect[1][1]
    s1, s2 = Solver.solve_quadratics(self, a, b, c)
    s1 = Solver.check_legal_root(s1, s2)
    t = (self.dst_point[1] - self.vertex_rect[0][1] - y41 * s) / (self.vertec_rect[1][1] + y32 * s - self.vertex_rect[0][1] - y41 * s)
    self.wgt_lst[0] = (1 - s) * (1 - t)
    self.wgt_lst[1] = (1 - s) * t
    self.wgt_lst[2] = s * t
    self.wgt_lst[3] = s * (1 - t)
   
   
  #         1---2     1---2
  # solve  /   /  or  |   | case
  #       0---3       0---3
  def solve_bilinear_case3(self):
    print 'I am in case3.'
    s = (self.dst_point[0] - self.vertex_rect[0][0]) / (self.vertex_rect[3][0] - self.vertex_rect[0][0])
    t = (self.dst_point[1] - self.vertex_rect[0][1]) / (self.vertex_rect[1][1] - self.vertex_rect[0][1])
    self.wgt_lst[0] = (1 - s) * (1 - t)
    self.wgt_lst[1] = (1 - s) * t
    self.wgt_lst[2] = s * t
    self.wgt_lst[3] = s * (1 - t)
    
  
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
    #print self.wgt_lst

