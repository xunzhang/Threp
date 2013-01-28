#! /usr/bin/python
# Filename: predictor.py

''' '''

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import numpy as np
import sys

class Predictor(Exception):
  # solve linear equation: Ax = b
  def __init__(self, dst_point, neighbor_lst):
    self.dst_point = dst_point
    self.neighbor_lst = neighbor_lst
    self.wgt_lst = []

  def predict(self):
    pass

