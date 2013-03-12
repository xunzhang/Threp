#! /usr/bin/python
# Filename: build.py

'''build.py: class Build defines to init a kdtree based on the grid coords info.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

#import sys
#import numpy as np
#sys.path.append("../search/")
from kdtree import KDTree
#from scipy import spatial

class Build(Exception):
  
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
    coords_pair_lst = zip(self.grid_center_lon, self.grid_center_lat)
    return coords_pair_lst
  
  # logical rectangle only, by now 
  def __add_ghost_boundary(self):
    # now I just add one layer ghost
    ghost_point_lat_lst = []
    ghost_point_lon_lst = []
    # trav every lat, set leftest boundary
    for i in xrange(self.grid_dims[1]):
      # insert rightest ghost point
      ghost_point_lat_lst.append(self.grid_center_lat[i + i * self.grid_dims[0]])
      ghost_point_lon_lst.append(self.grid_center_lon[0] + 360)
    # trav every lat, set rightest boundary 
    for i in xrange(self.grid_dims[1]):
      # insert leftest ghost point
      ghost_point_lat_lst.append(self.grid_center_lat[i + i * self.grid_dims[0]])
      ghost_point_lon_lst.append(self.grid_center_lon[self.grid_dims[0] - 1] - 360)
    
    # insert ghost_point_lst to grid_center_lst
    for lat in ghost_point_lat_lst:
      self.grid_center_lat.append(lat)
    for lon in ghost_point_lon_lst:
      self.grid_center_lon.append(lon)
    # append relative mask value
    for i in xrange(len(ghost_point_lat_lst)):
      self.grid_imask.append(1)
    
  def grow(self):
    self.__add_ghost_boundary()
    coords_pair_lst = self.__gen_coords_pair_lst()
    stree = KDTree(coords_pair_lst)
    #stree = spatial.KDTree(coords_pair_lst)
    #print stree.data
    return stree
    
if __name__ == '__main__':
  grid_size = 6
  grid_corners = 4
  grid_rank = 2
  grid_dims = [2, 3]
  grid_center_lon = [0.5, 0.5, 0.5, 359.5, 359.5, 359.5]
  grid_center_lat = [1.0, 2.0, 3.0, 1.0, 2.0, 3.0] 
  grid_imask = [1, 1, 0, 0, 1, 0]
  stree_base_obj = Build(grid_size, grid_corners, grid_rank, grid_dims, grid_center_lat, grid_center_lon, grid_imask)
  stree = stree_base_obj.grow()
  
  pts = np.array([[2.0, 2.0]])
  print stree.query(pts) 
  print stree.query_ball_point([[1.0, 1.0], [2.0, 2.0]], 300.0)
  
