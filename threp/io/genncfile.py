#! /usr/bin/python
# Filename: genncfile.py

''' '''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import sys
import time
import scipy
import numpy as np
from numpy import dtype
from Scientific.IO.NetCDF import NetCDFFile as Dataset 

class Genncfile(Exception):
   
  def __init__(self, filename, remap_obj, methodname):
    self.fname = filename
    self.obj = remap_obj
    self.method = methodname
  
  def gen(self):
    ncfile = Dataset(self.fname, 'w')
    tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    
    # set dimension info 
    ncfile.createDimension('grid_size', self.obj.grid_size)
    
    # set variable info
    grid_center_lat_var = ncfile.createVariable('grid_center_lat', dtype('d').char, ('grid_size',))
    grid_center_lon_var = ncfile.createVariable('grid_center_lon', dtype('d').char, ('grid_size',))
    physical_variable = ncfile.createVariable('physical_variable', dtype('d').char, ('grid_size',))
    
    grid_center_lat_var[:] = np.array(self.obj.grid_center_lat)
    grid_center_lon_var[:] = np.array(self.obj.grid_center_lon)
    physical_variable[:] = np.array(self.obj.physical_variable)
     
    setattr(ncfile, 'title', 'Threp ' + self.fname)
    setattr(ncfile, 'createdate', tm)
    setattr(ncfile, 'map_method', self.method)
    setattr(ncfile, 'conventions', 'Threp')
    setattr(ncfile, 'src_grid', self.obj.src_grid_name)
    setattr(ncfile, 'dst_grid', self.obj.dst_grid_name)
    
    ncfile.close() 
    print '*** Successfully generated netcdf file for ncl usage. ***'
