#! /usr/bin/python
# Filename: nearest.py

'''nearest.py: class nearest defines to find the nearest k-points of the query points in a kdtree.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import kdtree

class Search(Exception):

  def __init__(self, stree_base, stree):
    self.stree_base = stree_base
    self.stree = stree
    self.dist = 0.5
    self.delta = 0.25
  
  def find_nearest_k(self, query_point, k = 4):
    result_lst = []
    query = [query_point]
    # query in search tree.
    dist = self.dist
    result_indx = self.stree.query_ball_point(query, dist)
    while len(result_indx[0]) < k:
      result_indx = self.stree.query_ball_point(query, dist)
      dist += self.delta
    result_indx = result_indx[0][0 : k]
    # generate result coord pairs.
    for indx in result_indx:
      result_lst.append((self.stree_base.grid_center_lon[indx], self.stree_base.grid_center_lat[indx]))
    return result_indx, result_lst

  def find_nearest_dist(self, query_point, dist = 0.5):
    result_lst = []
    query = [query_point]
    result_indx = self.stree.query_ball_point(query, dist)
    for indx in result_indx:
      result_lst.append((self.stree_base.grid_center_lon[indx], self.stree_base.grid_center_lat[indx]))
    return result_indx, result_lst
  
  def find_nearest_triangle(self, query_point, threshold):
    pass
  
if __name__ == '__main__':
  pass   
