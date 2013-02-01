#! /usr/bin/python
# Filename: modify_filter.py
# Modify global attribute: title.
# Notice a potential bug: if variables have a units:radians, it may be replaced by degrees, so avoid it using indflag!

import time
from Scientific.IO.NetCDF import NetCDFFile as Dataset

def modify_filter(gridfilename, ttlname, indflag = 1):

  tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

  ncfile = Dataset(gridfilename, 'a')

  if indflag:
    grid_center_lat_var = ncfile.variables['grid_center_lat']
    setattr(grid_center_lat_var, 'units', 'degrees')
    grid_center_lon_var = ncfile.variables['grid_center_lon']
    setattr(grid_center_lon_var, 'units', 'degrees')
    grid_corner_lat_var = ncfile.variables['grid_corner_lat']
    setattr(grid_corner_lat_var, 'units', 'degrees')
    grid_corner_lon_var = ncfile.variables['grid_corner_lon']
    setattr(grid_corner_lon_var, 'units', 'degrees')
  
  setattr(ncfile, 'title', ttlname)
  setattr(ncfile, 'modifydate', tm)

  if hasattr(ncfile, 'grid_name'):
    delattr(ncfile, 'grid_name')

  if hasattr(ncfile, 'map_method'):
    delattr(ncfile, 'map_method')

  ncfile.sync()
  ncfile.close()


if __name__ == '__main__':
  path = '../../grid/factory/'
  grid_file_name_lst = ['T42.nc', 'Gamil_360x180_Grid.nc', 'Gamil_128x60_Grid.nc', 'T62_Gaussian_Grid.nc', 'T85_Gaussian_Grid.nc', 'll1deg_grid.nc', 'll2.5deg_grid.nc', 'POP43.nc', 'licom_eq1x1_degree_Grid.nc', 'licom_gr1x1_degree_Grid.nc', 'LICOM_P5_Grid.nc', 'gx3v5_Present_DP_x3.nc', 'R05_Grid.nc', 'R42_Gaussian_Grid.nc']
  ttlname_lst = ['Threp T42 Gaussian Grid', 'Threp GAMIL360x180 Grid', 'Threp GAMIL128x60 Grid', 'Threp T62 Gaussian Grid', 'Threp T85 Gaussian Grid', 'Threp Lat/lon 1 degree Grid', 'Threp Lat/lon 2.5 degree Grid', 'Threp POP 4/3 Displaced-Pole T grid', 'Threp licom eq1x1 Grid', 'Threp licom gr1x1 Grid', 'Threp LICOM P5 Grid', 'Threp gx3v5 Present DP x3 Grid', 'Threp R05 Grid', 'Threp R42 Gaussian Grid']
  indflag_lst = [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1]
  n = len(indflag_lst)
  for i in range(n):
    gridfilename = path + grid_file_name_lst[i]
    modify_filter(gridfilename, ttlname_lst[i], indflag_lst[i])
