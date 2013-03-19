#! /usr/bin/python
# Filename: loadnc.py

'''loadnc.py: class Loadnc defines to load grid data from a SCRIP format NetCDF file.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import re
import sys
import math
#from Scientific.IO.NetCDF import NetCDFFile as Dataset 
from Scientific_netcdf import NetCDFFile as Dataset

class Loadnc(Exception):
  
  def __init__(self, file_name):
    ''' Initialize grid file object.
        Open a netCDF file for reading.'''
    self.filename = file_name
    self.ncfile = Dataset(file_name, 'r')

  def closenc(self):
    ''' Close the file.'''
    self.ncfile.close()    

  def load(self):
    '''load all dimensions and variables info.'''
    # load dimension info.
    grid_size = self.__get_grid_size()
    grid_corners = self.__get_grid_corners()
    grid_rank = self.__get_grid_rank()
 
    # load variable info.
    grid_dims = self.__get_grid_dims()
    [grid_center_lat, grid_center_lon] = self.__get_grid_center_coords()
    grid_imask = self.__get_grid_imask()
   
    # check dimension info.
    cond = grid_size > 0 and grid_corners > 0 and grid_rank and grid_size == grid_dims[0] * grid_dims[1] 
    if cond:
      print '***Successfully reading dimension info from netCDF file %s.*** ' % self.filename
    else: 
      print '***Dimension info is invalid.***'
      sys.exit()
    # check dimension info.
    cond = len(grid_center_lat) == grid_size and len(grid_center_lon) == grid_size and len(grid_imask) == grid_size
    if cond:
      print '***Successfully reading variable info from netCDF file %s.*** ' % self.filename
    else: 
      print '***Dimension info is invalid.***'
    return grid_size, grid_corners, grid_rank, grid_dims, grid_center_lat, grid_center_lon, grid_imask
     
  def __get_grid_size(self):
    dimension_name = 'grid_size'
    __grid_size = self.ncfile.dimensions[dimension_name]
    return __grid_size

  def __get_grid_corners(self):
    dimension_name = 'grid_corners'
    __grid_corners = self.ncfile.dimensions[dimension_name]
    return __grid_corners

  def __get_grid_rank(self):
    dimension_name = 'grid_rank'
    __grid_rank = self.ncfile.dimensions[dimension_name]
    return __grid_rank
  
  def __get_grid_dims(self):
    variable_name = 'grid_dims'
    __grid_dims = self.ncfile.variables[variable_name][:]
    return __grid_dims

  def __get_grid_center_coords(self):
    variable_name = 'grid_center_lat'
    __grid_center_lat = self.ncfile.variables[variable_name][:]
    variable_name = 'grid_center_lon'
    __grid_center_lon = self.ncfile.variables[variable_name][:]
    __grid_center_lat = __grid_center_lat.tolist()
    __grid_center_lon = __grid_center_lon.tolist()
    
    # transform radians to degrees
    if re.findall('r?R?ad', self.ncfile.variables[variable_name].units):
      __grid_center_lat = [item * 180 / math.pi for item in __grid_center_lat]
      __grid_center_lon = [item * 180 / math.pi for item in __grid_center_lon]
      
    return __grid_center_lat, __grid_center_lon
    
  def __get_grid_imask(self):
    variable_name = 'grid_imask'
    __grid_imask = self.ncfile.variables[variable_name][:]
    __grid_imask = __grid_imask.tolist()
    
    oc_num = 0
    ld_num = 0
    #for mask in __grid_imask:
    #  if mask == 0:
    #    oc_num += 1
    #  else:
    #    ld_num += 1
    #print 'oc_num'
    #print oc_num
    #print 'ld_num'
    #print ld_num
    return __grid_imask
  
  def __get_grid_corner_coords(self):
    pass

  def __get_grid_frac(self):
    pass

if __name__ == '__main__':
  nc_obj = Loadnc('../grid/T42.nc')
  grid_size, grid_corners, grid_rank, grid_dims, grid_center_lat, grid_center_lon, grid_imask = nc_obj.load()
  nc_obj.closenc()
  print grid_size
  print grid_corners
  print grid_rank
  print grid_dims[0]
  print grid_dims[1]
  print grid_center_lat[128]
  print grid_center_lon[1]
  print grid_imask[0]
