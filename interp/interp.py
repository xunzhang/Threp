#! /usr/bin/python
# Filename: interp.py

import threp_import
from loadnc import Loadnc
from build import Build

class Interp(Exception):
  
  def __init__(self, src_grid_file_name, dst_grid_file_name):
    src_nc_obj = Loadnc(src_grid_file_name)
    self.src_grid_size, self.src_grid_corners, self.src_grid_rank, self.src_grid_dims, self.src_grid_center_lat, self.src_grid_center_lon, self.src_grid_imask = src_nc_obj.load()
    src_nc_obj.closenc()
    
    dst_nc_obj = Loadnc(dst_grid_file_name)
    self.dst_grid_size, self.dst_grid_corners, self.dst_grid_rank, self.dst_grid_dims, self.dst_grid_center_lat, self.dst_grid_center_lon, self.dst_grid_imask = dst_nc_obj.load()
    dst_nc_obj.closenc()
    
    self.stree_base_obj = Build(self.src_grid_size, self.src_grid_corners, self.src_grid_rank, self.src_grid_dims, self.src_grid_center_lat, self.src_grid_center_lon, self.src_grid_imask)
    self.stree = self.stree_base_obj.grow()
    
  # for example, decide if it is land cell
  def check_all_masks(self, indx, n):
    checksum = 0
    for i in indx:
      if self.src_grid_imask[i] == 0:
        checksum += 1
    if checksum == n:
      return True
    else:
      return False
  
  def indx_recovery(self, indx_lst):
    tmp_indx = []
    for i in indx_lst:
      if i >= self.src_grid_size:
        print 'recovery ghost index.'
        if (i / self.src_grid_dims[1]) == 1:
          offset = 0
        else:
          offset = self.src_grid_dims[0] - 1
        tmp_indx.append((i % self.src_grid_dims[1]) * self.src_grid_dims[0] + offset)
    indx_lst = tmp_indx
      
  # virtual function to do calc wgts  
  def interp(self):
    pass
    
  # virtual function to remap data 
  def remap(self):
    pass
     

