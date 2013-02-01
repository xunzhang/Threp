#! /usr/bin/python
# Filename: gen_gx1v1.py
# Notice: no corner info be contained.

import time
import scipy
import copy
from numpy import dtype
from Scientific.IO.NetCDF import NetCDFFile as Dataset

ncfile = Dataset('../../grid/CPLDATA/X02.cpl6.ha.0007-07.nc', 'r')
nc = Dataset('gx1v1.nc', 'w')
tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
nx = 360; ny = 200
grid_size = ncfile.dimensions['n_o']
grid_rank = ncfile.dimensions['d2']

# load data
#dims = ncfile.variables['grid_dims'][:]
dims = scipy.array([nx, ny])
lat = ncfile.variables['domain_o_lat'][:, :]
tmp = []
for i in range(ny):
  for j in range(nx):
   tmp.append(lat[i][j])
lat = scipy.array(tmp)

lon = ncfile.variables['domain_o_lon'][:, :]
tmp = []
for i in range(ny):
  for j in range(nx):
   tmp.append(lon[i][j])
lon = scipy.array(tmp)

imask = ncfile.variables['domain_o_mask'][:, :]
tmp = []
for i in range(ny):
  for j in range(nx):
   tmp.append(int(imask[i][j]))
imask = scipy.array(tmp)

# create dimensions
nc.createDimension('grid_size', 72000)
nc.createDimension('grid_rank', 2)
nc.createDimension('grid_corners', 4)

# create variables
grid_dims_var = nc.createVariable('grid_dims', dtype('int32').char, ('grid_rank',))
lat_var = nc.createVariable('grid_center_lat', dtype('d').char, ('grid_size',))
lat_var.units = 'degrees'
lon_var = nc.createVariable('grid_center_lon', dtype('d').char, ('grid_size',))
lon_var.units = 'degrees'
grid_imask_var = nc.createVariable('grid_imask', dtype('int32').char, ('grid_size',))
grid_imask_var.units = 'unitless'

grid_dims_var[:] = dims 
lat_var[:] = lat 
lon_var[:] = lon
grid_imask_var[:] = imask

setattr(nc, 'title', 'Threp gx1v1 Grid')
setattr(nc, 'modifydate', tm)

nc.close()
ncfile.close()
print '*** Success generating example file gx1v1.nc'
