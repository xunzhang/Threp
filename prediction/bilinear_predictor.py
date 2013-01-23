#! /usr/bin/python
# Filename: bilinear_predictor.py

''' '''

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import numpy as np
from predictor import Predictor

class Bilinear_Predictor(Predictor):
  # solve linear equation: Ax = b
  def __init__(self, dst_point, vertex_box):
    Predictor.__init__(self, dst_point, vertex_box)
    self.vertex_box = self.neighbor_lst
    matrix_str = self.__genmatrix()
    self.A = np.matrix(matrix_str)
  
  # Suppose local bilinear function f((x, y)) = a + b * x + c * y + d * x * y
  #            [ 1 x1 y1 x1y1 ]
  # matrix A = [ 1 x2 y2 x2y2 ]
  #            [ 1 x3 y3 x3y3 ]
  #            [ 1 x4 y4 x4y4 ]
  def __genmatrix(self):
    row1 = [1, self.vertex_box[0][0], self.vertex_box[0][1], self.vertex_box[0][0] * self.vertex_box[0][1]]
    row2 = [1, self.vertex_box[1][0], self.vertex_box[1][1], self.vertex_box[1][0] * self.vertex_box[1][1]]
    row3 = [1, self.vertex_box[2][0], self.vertex_box[2][1], self.vertex_box[2][0] * self.vertex_box[2][1]]
    row4 = [1, self.vertex_box[3][0], self.vertex_box[3][1], self.vertex_box[3][0] * self.vertex_box[3][1]]
    row1 = [str(item) for item in row1]
    row2 = [str(item) for item in row2]
    row3 = [str(item) for item in row3]
    row4 = [str(item) for item in row4]
    row1_str = ' '.join(row1) 
    row2_str = ' '.join(row2) 
    row3_str = ' '.join(row3) 
    row4_str = ' '.join(row4) 
    return row1_str + ';' + row2_str + ';' + row3_str + ';' + row4_str 
    
  def predict(self):
    dst_pnt_vec = np.matrix('1 ' + str(self.dst_point[0]) + ' ' + str(self.dst_point[1]) + ' ' + str(self.dst_point[0] * self.dst_point[1]))
    print self.A
    inv_A = np.linalg.inv(self.A)
    wgt = dst_pnt_vec * inv_A
    self.wgt_lst = wgt.tolist()[0]
    
