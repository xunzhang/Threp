#! /usr/bin/python
# Filename: bilinearbox.py

'''bilinearbox.py: class nearest defines to find the nearest k-points of the query points in a kdtree.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import sys
from matplotlib.path import Path
from nearest import Search
from selectrect import select_containing_rect

class Bilinearbox(Search):

  def __init__(self, stree_base, stree):
    Search.__init__(self, stree_base, stree)
    self.threshold = 5.0
    self.outside = True
  
  def reorder(self, coords_lst):
    '''
    B---D
    |   |
    A---C
    '''
    # check the input lst
    if len(coords_lst) != 4:
      print 'invalid input in reorder func.'
      sys.exit()
    # use default sort of 4 tuples, by cmp the first dim
    coords_lst.sort()
    # reorder A,B & C,D
    if coords_lst[0][1] > coords_lst[1][1]:
      coords_lst[0], coords_lst[1] = coords_lst[1], coords_lst[0]
    if coords_lst[2][1] > coords_lst[3][1]:
      coords_lst[2], coords_lst[3] = coords_lst[3], coords_lst[2]
  
  def filter_mask(self, indx, lst):
    a = []
    b = []
    for i in range(len(indx)):
      # if mask is 1
      if self.stree_base.grid_imask[indx[i]]:
        a.append(indx[i])
        b.append(lst[i])
    return a, b
  
  # prevent all masked out in bilinear.py(before calling this function) 
  def find_nearest_box(self, query_point):
    # find nearest 16
    res_indx, res_lst = Search.find_nearest_k(self, query_point, 16)
    # filter the masked points
    res_indx, res_lst = self.filter_mask(res_indx, res_lst)
    # find bilinear_box 
    flag, box_indx, box = select_containing_rect(query_point, res_indx, res_lst)
    self.outside = flag
    self.reorder(box)
    #self.reorder(box_indx, box)
    return self.outside, box_indx, box
      
if __name__ == '__main__':
  test_tuple = [(-1,2), (0,0), (2,0), (3,4)]
  #reorder(test_tuple)
  print test_tuple
