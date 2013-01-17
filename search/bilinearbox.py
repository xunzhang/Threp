#! /usr/bin/python
# Filename: bilinearbox.py

'''bilinearbox.py: class nearest defines to find the nearest k-points of the query points in a kdtree.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import sys
from matplotlib.path import Path
from nearest import Search

class Bilinearbox(Search):

  def __init__(self, stree_base, stree):
    Search.__init__(self, stree_base, stree)
    self.threshold = 5.0
    self.outside = True
  
  #Path([[0, 1], [1, 1], [1, 0], [0, 0]]).contains_point([0.5, 0.5])
  def is_contain(self, query_point, vertex_lst):
    cond = Path(vertex_lst).contains_point(query_point) or query_point in vertex_lst
    if cond:
      return True
    else:
      return False

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
  
  def find_nearest_box(self, query_point):
    box = []
    res_indx, res_lst = Search.find_nearest_k(self, query_point, 4)
    if self.is_contain(query_point, res_lst):
      self.outside = False
      print 'Successfully contains.'
      #if not is_contain(query_point, res_lst):
      #res_indx, res_lst = Search.find_nearest_k(query_point, 20)
      # to be coded a algorithm
      #while
      #  if distance2d() > self.threshold:
      #    pass
      #  print 'Can not find nearest box containing the query point.'
    box = res_lst
    self.reorder(box)
    print box
    return self.outside, box
    
if __name__ == '__main__':
  test_tuple = [(-1,2), (0,0), (2,0), (3,4)]
  #reorder(test_tuple)
  print test_tuple
