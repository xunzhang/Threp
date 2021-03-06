#! /usr/bin/python
# Filename: bilinearbox.py

'''bilinearbox.py: class nearest defines to find the nearest k-points of the query points in a kdtree.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import sys
#from matplotlib.path import Path
from nearest import Search
from selectrect import select_containing_rect
from clockwise_sort import clockwise_sort
from clockwise_sort import clockwise_sort_indx

class Bilinearbox(Search):

  def __init__(self, stree_base, stree):
    Search.__init__(self, stree_base, stree)
    self.threshold = 5.0
    self.outside = True
    self.full = True
  
  def filter_mask(self, indx, lst):
    a = []
    b = []
    for i in xrange(len(indx)):
      # if mask is 1
      if self.stree_base.grid_imask[indx[i]]:
        a.append(indx[i])
        b.append(lst[i])
    return a, b
  
  # prevent all masked out in bilinear.py(before calling this function) 
  def find_nearest_box(self, query_point):
    # find nearest 24
    res_indx, res_lst = Search.find_nearest_k(self, query_point, 24)
    # filter the masked points
    res_indx, res_lst = self.filter_mask(res_indx, res_lst)
    if len(res_indx) < 4:
      self.full = False
    # find bilinear_box 
    flag, box_indx, box = select_containing_rect(query_point, res_indx, res_lst)
    self.outside = flag
    if flag:
      print 'Can not be contained.'
    else:
      box_indx, box = clockwise_sort_indx(box_indx, box)
      box = clockwise_sort(box)
    return self.outside, self.full, box_indx, box
      
if __name__ == '__main__':
  test_tuple = [(-1,2), (0,0), (2,0), (3,4)]
  #reorder(test_tuple)
  print test_tuple
