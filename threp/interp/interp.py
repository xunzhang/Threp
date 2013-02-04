#! /usr/bin/python
# Filename: interp.py

import copy
import threp_import
from loadnc import Loadnc
from loadreal import Loadreal
from build import Build

class Interp(Exception):
  
  def __init__(self, src_grid_file_name, dst_grid_file_name, online_flag, src_realdata_file_name):
    src_nc_obj = Loadnc(src_grid_file_name)
    self.src_grid_size, self.src_grid_corners, self.src_grid_rank, self.src_grid_dims, self.src_grid_center_lat, self.src_grid_center_lon, self.src_grid_imask = src_nc_obj.load()
    src_nc_obj.closenc()

    # original grid info
    # used for remap matrix file
    self.original_src_grid_center_lat = copy.deepcopy(self.src_grid_center_lat)
    self.original_src_grid_center_lon = copy.deepcopy(self.src_grid_center_lon)
    self.original_src_grid_imask = copy.deepcopy(self.src_grid_imask)
     
    dst_nc_obj = Loadnc(dst_grid_file_name)
    self.dst_grid_size, self.dst_grid_corners, self.dst_grid_rank, self.dst_grid_dims, self.dst_grid_center_lat, self.dst_grid_center_lon, self.dst_grid_imask = dst_nc_obj.load()
    dst_nc_obj.closenc()
    
    self.stree_base_obj = Build(self.src_grid_size, self.src_grid_corners, self.src_grid_rank, self.src_grid_dims, self.src_grid_center_lat, self.src_grid_center_lon, self.src_grid_imask)
    self.stree = self.stree_base_obj.grow()
    
    self.src_grid_name = src_grid_file_name.split('/')[-1].split('.')[0]
    self.dst_grid_name = dst_grid_file_name.split('/')[-1].split('.')[0]
     
    #self.interp_wgt = []
    #self.interp_box_indx = []
    #self.interp_box = []
    self.remap_matrix = []
    self.remap_matrix_indx = []
    
    self.remap_matrix_compact = []
    self.remap_src_indx = []
    self.remap_dst_indx = []
    
    # load real data if online remapping
    # self.src_data = []
    if online_flag:
      src_data_nc_obj = Loadreal(src_realdata_file_name)
      size, self.src_data = src_data_nc_obj.load()
      if size != self.src_grid_size:
        print 'Real data size does not match grid size.'
        sys.exit()
      src_data_nc_obj.closenc()
    
    self.dst_data = [] 
   
  # decide if all indx cells are masked out
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
        flag = True
        print 'recovery ghost index.'
        if (i / self.src_grid_dims[1]) == 1:
          offset = 0
        else:
          offset = self.src_grid_dims[0] - 1
        tmp_indx.append((i % self.src_grid_dims[1]) * self.src_grid_dims[0] + offset)
      else:
        tmp_indx.append(i)
    indx_lst = tmp_indx
    return indx_lst
      
  # virtual function to do calc wgts  
  def interp(self):
    pass
    
  # virtual function to interpolate data 
  def remap(self):
    for i in range(len(self.remap_matrix_compact)):
      self.dst_data[self.remap_dst_indx[i]] += self.remap_matrix_compact[i] * self.src_data[remap_src_indx[i]]
    return dst_data
     
  def compact_remap_matrix(self):
    i = 0
    k = 0
    for matrix_item in self.remap_matrix:
      if matrix_item:
        j = 0
        for wgt in matrix_item:
          self.remap_matrix_compact.append(wgt)
          self.remap_src_indx.append(self.remap_matrix_indx[i][j])
          self.remap_dst_indx.append(k)
          j += 1
      k += 1
      i += 1  
    
