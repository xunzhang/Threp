#! /usr/bin/python
# Filename: nearest.py

'''nearest.py: class nearest defines to find the nearest k-points of the query points in a kdtree.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import nearest
Search.find_nearest_k(query_point, k = 4):
Search.find_nearest_dist(query_point, dist = 0.5):

class Bilinearbox(Search):

  def __init__(self, stree_base, stree):
    Search.__init__(self, stree_base, stree)
    self.threshold = 5.0
    self.outside = True
  
  def is_contain(self, query_point, vertex_lst):
    
  def reorder(self, coords_lst):
  '''
  C---D
  |   |
  A---B
  '''
  
  def find_nearest_box(self, query_point):
    box = []
    res_indx, res_lst = Search.find_nearest_k(query_point, 4)
    if not is_contain(query_point, res_lst):
      res_indx, res_lst = Search.find_nearest_k(query_point, 20)
      # to be coded a algorithm
      while
        if distance2d() > self.threshold:
          pass
        print 'Can not find nearest box containing the query point.'
        self.outside = True
    reorder(box)
    return box
    
if __name__ == '__main__':
  pass   
