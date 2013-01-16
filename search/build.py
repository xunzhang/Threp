#! /usr/bin/python
# Filename: build.py

'''build.py: class build defines to init a kdtree based on the grid coords info.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import numpy as np
from scipy import spatial

class build(Exception):
  
  def __init__(self, grid_size, grid_corners, grid_rank, grid_dims, grid_center_lat, grid_center_lon, grid_imask):
    '''Comments'''
    self.grid_size = grid_size
    self.grid_corners = grid_corners
    self.grid_rank = grid_rank
    self.grid_dims = grid_dims
    self.grid_center_lat = grid_center_lat
    self.grid_center_lon = grid_center_lon
    self.grid_imask = grid_imask
  
  def __gen_coords_pair_lst(self):
    coords_pair_lst = zip(self.grid_center_lat, self.grid_center_lon)
    return coords_pair_lst
    
  def grow(self):
    coords_pair_lst = self.__gen_coords_pair_lst()
    stree = spatial.KDTree(coords_pair_lst)
    # print stree.data
    return stree
  
if __name__ == '__main__':
  grid_size = 6
  grid_corners = 4
  grid_rank = 2
  grid_dims = [2, 3]
  grid_center_lat = [1.0, 1.0, 1.0, 3.0, 3.0, 3.0] 
  grid_center_lon = [1.0, 2.0, 3.0, 1.0, 2.0, 3.0]
  grid_imask = [1, 1, 0, 0, 1, 0]
  stree_base_obj = build(grid_size, grid_corners, grid_rank, grid_dims, grid_center_lat, grid_center_lon, grid_imask)
  stree = stree_base_obj.grow()
  
  #pts = np.array([[2.0, 2.0]])
  #print stree.query(pts) 
  #print stree.query_ball_point([2.0, 2.0], 1.0)
  
