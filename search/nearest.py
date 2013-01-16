#! /usr/bin/python
# Filename: nearest.py

'''nearest.py: class nearest defines to find the nearest k-points of the query points in a kdtree.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import kdtree
  
def find_nearest_k(stree_base, stree, query_point, k = 4):
  result_lst = []
  query = [query_point]
  # query in search tree.
  dist = 0.5
  while len(result_indx) < k:
    result_indx = stree.query_ball_point(query, dist)
    dist += 0.25
  result_indx = result[0 : k]
  # generate result coord pairs.
  for indx in result_indx:
    result_lst.append((stree_base.grid_center_lon[indx], stree_base.grid_center_lat[indx]))
  return result_lst

def find_nearest_dist(stree_base, stree, query_point, dist = 0.5):
    result_lst = []
    query = [query_point]
    result_indx = stree.query_ball_point(query, dist)
    for indx in result_indx:
      result_lst.append((stree_base.grid_center_lon[indx], stree_base.grid_center_lat[indx]))
    return result_lst

if __name__ == '__main__':
  pass   
