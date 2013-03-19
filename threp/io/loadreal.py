#! /usr/bin/python
# Filename: loadreal.py

''' loadreal.py: load read data from NetCDF files.'''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

#from Scientific.IO.NetCDF import NetCDFFile as Dataset
from Scientific_netcdf import NetCDFFile as Dataset

class Loadreal(Exception):
  
  def __init__(self, file_name):
    self.filename = file_name
    self.ncfile = Dataset(file_name, 'r')
  
  def closenc(self):
    self.ncfile.close()
  
  def load(self):
    dimension_name = 'grid_size'
    grid_size = self.ncfile.dimensions[dimension_name]
    variable_name = 'data'
    data = self.ncfile.variables[variable_name][:]
    return grid_size, data
    
if __name__ == '__main__':
  nc_obj = Loadreal('../../data/real/T42_Gaussian_Grid/T42_avXa2c_a_Faxa_lwdn-0006-12.nc')
  size, data = nc_obj.load()
  print len(data)
  nc_obj.closenc()
 
