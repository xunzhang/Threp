#! /usr/bin/python
# Filename: writenc.py

''' '''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import sys
import time
import scipy
import numpy as np
from numpy import dtype
from Scientific.IO.NetCDF import NetCDFFile as Dataset 
from loadnc import Loadnc

class CoordTransfer(Exception):
  def __init__(self, srcfile, dstfile, newfile):
    self.srcfile = srcfile
    self.dstfile = dstfile
    self.newfile = newfile
    
  def loadsrcoords(self):
    self.ncfile = Dataset(self.srcfile, 'r')
    variable_name = 'grid_center_lat'
    __grid_center_lat = self.ncfile.variables[variable_name][:]
    variable_name = 'grid_center_lon'
    __grid_center_lon = self.ncfile.variables[variable_name][:]
    self.__grid_center_lat = __grid_center_lat.tolist()
    self.__grid_center_lon = __grid_center_lon.tolist()
    
  def loadstinfo(self):
   self.nc_obj = Loadnc(self.dstfile)
   self.grid_size, self.grid_corners, self.grid_rank, self.grid_dims, ach1, ach2, self.grid_imask = self.nc_obj.load()
   
  def transfercoord(self):
    self.resncfile = Dataset(self.newfile, 'w')
    tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    
    # set dimension info 
    self.resncfile.createDimension('grid_size', self.grid_size)
    self.resncfile.createDimension('grid_rank', self.grid_rank)
    self.resncfile.createDimension('grid_corners', self.grid_corners)

    # set variable info
    grid_dims_var = self.resncfile.createVariable('grid_dims', dtype('int32').char, ('grid_rank',))
    grid_center_lat_var = self.resncfile.createVariable('grid_center_lat', dtype('d').char, ('grid_size',))
    grid_center_lat_var.units = 'degrees'
    grid_center_lon_var = self.resncfile.createVariable('grid_center_lon', dtype('d').char, ('grid_size',))
    grid_center_lon_var.units = 'degrees'
    grid_imask_var = self.resncfile.createVariable('grid_imask', dtype('i').char, ('grid_size',))
    grid_imask_var.units = 'unitless'

    grid_dims_var[:] = self.grid_dims
    grid_center_lat_var[:] = np.array(self.__grid_center_lat)
    grid_center_lon_var[:] = np.array(self.__grid_center_lon)
    buffer1 = [np.int32(i) for i in self.grid_imask]
    grid_imask_var[:] = np.array(buffer1)

    setattr(self.resncfile, 'title', 'Threp ' + self.newfile)
    setattr(self.resncfile, 'createdate', tm)
    setattr(self.resncfile, 'conventions', 'Threp')
    setattr(self.resncfile, 'grid', self.newfile)

  def finish(self):
    self.resncfile.close()
    self.nc_obj.closenc()


if __name__ == '__main__':
  obj = CoordTransfer('../../tools/Threp_Validate/avXa2c_a_Sa_ptem.T42.nc', '../../grid/masked_T42_Gaussian_POP43/T42_Gaussian_mask.nc', 'realdataT42_masked.nc') 
  #obj = CoordTransfer('../../tools/Threp_Validate/avXa2c_a_Sa_ptem.T42.nc', '../../grid/T42.nc', 'realdataT42.nc') 
  #obj = CoordTransfer('../../tools/Threp_Validate/avXa2c_a_Sa_ptem.POP43.nc', '../../grid/POP43.nc', 'realdataPOP43.nc') 
  obj.loadsrcoords()
  obj.loadstinfo()
  obj.transfercoord()
  obj.finish()
