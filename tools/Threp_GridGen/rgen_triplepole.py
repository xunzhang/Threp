#! /usr/bin/python
# Filename: rgen_triplepole.py

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import time
import scipy
from numpy import dtype
from Scientific.IO.NetCDF import NetCDFFile as Dataset

ncfile = Dataset('../../grid/More/Ocean_p50_for_SCRIP.nc', 'r')
nc = Dataset('Ocean_p50_triplepole.nc', 'w')
tm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
nx = 720; ny = 410
grid_size = ncfile.dimensions['grid_size']
grid_rank = ncfile.dimensions['grid_rank']

# load data
dims = scipy.array([nx, ny])

lat = ncfile.variables['grid_center_lat'][:]
tmp = []
for i in xrange(nx * ny):
  if lat[i] < 0:
    lat[i] += 360
  tmp.append(lat[i])
lon_adjust = scipy.array(tmp)

lon = ncfile.variables['grid_center_lon'][:]
tmp = []
for i in xrange(nx * ny):
  tmp.append(lon[i])
lat_adjust = scipy.array(tmp)

imask = ncfile.variables['grid_imask'][:]
tmp = []
for i in xrange(nx * ny):
  tmp.append(int(imask[i]))
imask = scipy.array(tmp)

# create dimensions
nc.createDimension('grid_size', nx * ny)
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
lat_var[:] = lat_adjust
lon_var[:] = lon_adjust
grid_imask_var[:] = imask
  
setattr(nc, 'title', 'Threp Oceanp50 triplepole Grid')
setattr(nc, 'modifydate', tm)
  
nc.close()
ncfile.close()
print '*** Success generating example file Ocean_p50_triplepole.nc'
