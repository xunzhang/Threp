#! /usr/bin/python
# Filename: writenc.py

''' '''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import sys
import time
import scipy
from numpy import dtype
from Scientific.IO.NetCDF import NetCDFFile as Dataset 

class Writenc(Exception):
   
  def __init__(self, filename, remap_obj, alg_name):
    self.fname = filename
    self.obj = remap_obj
    self.method = alg_name
    self.n_wgt = len(remap_obj.remap_matrix_compact)
  
  def write(self):
    ncfile = Dataset(self.fname, 'w')
    tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    
    # set dimension info 
    ncfile.createDimension('src_grid_size', self.obj.src_grid_size)
    ncfile.createDimension('dst_grid_size', self.obj.dst_grid_size)
    ncfile.createDimension('n_wgt', self.n_wgt)
    ncfile.createDimension('src_grid_rank', self.obj.src_grid_rank)
    ncfile.createDimension('dst_grid_rank', self.obj.dst_grid_rank)
    ncfile.createDimension('num_wgts', 1)
    ncfile.createDimension('src_grid_corners', self.obj.src_grid_corners)
    ncfile.createDimension('dst_grid_corners', self.obj.dst_grid_corners)
    
    # set variable info
    src_grid_dims_var = ncfile.createVariable('src_grid_dims', dtype('int32').char, ('src_grid_rank',))
    dst_grid_dims_var = ncfile.createVariable('dst_grid_dims', dtype('int32').char, ('dst_grid_rank',))
    src_grid_center_lat_var = ncfile.createVariable('src_grid_center_lat', dtype('d').char, ('src_grid_size',))
    src_grid_center_lon_var = ncfile.createVariable('src_grid_center_lon', dtype('d').char, ('src_grid_size',))
    dst_grid_center_lat_var = ncfile.createVariable('dst_grid_center_lat', dtype('d').char, ('dst_grid_size',))
    dst_grid_center_lon_var = ncfile.createVariable('dst_grid_center_lon', dtype('d').char, ('dst_grid_size',))
    src_grid_imask_var = ncfile.createVariable('src_grid_imask', dtype('int32').char, ('src_grid_size',))
    dst_grid_imask_var = ncfile.createVariable('dst_grid_imask', dtype('int32').char, ('dst_grid_size',))
    remap_src_indx_var = ncfile.createVariable('remap_src_indx', dtype('int32').char, ('n_wgt',))
    remap_dst_indx_var = ncfile.createVariable('remap_dst_indx', dtype('int32').char, ('n_wgt',))
    remap_matrix_var = ncfile.createVariable('remap_matrix', dtype('d').char, ('n_wgt',))
    
    src_grid_dims_var[:] = self.obj.src_grid_dims
    dst_grid_dims_var[:] = self.obj.dst_grid_dims
    print len(self.obj.original_src_grid_center_lat)
    src_grid_center_lat_var[:] = scipy.array(self.obj.original_src_grid_center_lat)
    src_grid_center_lon_var[:] = scipy.array(self.obj.original_src_grid_center_lon)
    dst_grid_center_lat_var[:] = scipy.array(self.obj.dst_grid_center_lat)
    dst_grid_center_lon_var[:] = scipy.array(self.obj.dst_grid_center_lon)
    src_grid_imask_var[:] = scipy.array(self.obj.original_src_grid_imask)
    dst_grid_imask_var[:] = scipy.array(self.obj.dst_grid_imask)
    remap_src_indx_var[:] = scipy.array(self.obj.remap_src_indx)
    remap_dst_indx_var[:] = scipy.array(self.obj.remap_dst_indx)
    remap_matrix_var[:] = scipy.array(self.obj.remap_matrix_compact)
    
    setattr(ncfile, 'title', 'Threp ' + self.fname)
    setattr(ncfile, 'createdate', tm)
    setattr(ncfile, 'map_method', self.method)
    setattr(ncfile, 'conventions', 'Threp')
    setattr(ncfile, 'src_grid', self.obj.src_grid_name)
    setattr(ncfile, 'dst_grid', self.obj.dst_grid_name)
    
    ncfile.close() 
    print '*** Successfully generate remap matrix file. ***'
