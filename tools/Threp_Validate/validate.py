#! /usr/bin/python
# Filename: validate.py

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import math
from Scientific.IO.NetCDF import NetCDFFile as Dataset

# 2 + cos(pi * r / L), 2 + cos(acos(-cos(lat) * cos(lon)) / 2)
def test_func1(lat, lon):
  val_tmp = -math.cos(lat) * math.cos(lon)
  return 2 + math.cos(math.acos(val_tmp) / 2) 

# 2 + cos(lat)^2 * cos(2lon)
def test_func2(lat, lon):
  return 2 + math.cos(lat) ** 2 * math.cos(2 * lon)  

# 2 + sin(2lat)^16 * cos(16lon)
def test_func3(lat, lon):
  return 2 + math.sin(2 * lat) ** 16 * math.cos(16 * lon)

def load_rmpwfile(fname):
  ncfile = Dataset(fname, 'r')
  src_coord_lat = ncfile.variables['src_grid_center_lat'][:].tolist()
  src_coord_lon = ncfile.variables['src_grid_center_lon'][:].tolist()
  dst_coord_lat = ncfile.variables['dst_grid_center_lat'][:].tolist()
  dst_coord_lon = ncfile.variables['dst_grid_center_lon'][:].tolist()
  remap_src_indx = ncfile.variables['remap_src_indx'][:].tolist()
  remap_dst_indx = ncfile.variables['remap_dst_indx'][:].tolist()
  remap_matrix_compact = ncfile.variables['remap_matrix'][:].tolist()
  ncfile.close()
  return src_coord_lat, src_coord_lon, dst_coord_lat, dst_coord_lon, remap_src_indx, remap_dst_indx, remap_matrix_compact

if __name__ == '__main__':
  #filename = 'rmp_POP43_T42_Gaussian_idw.nc'
  #filename = 'rmp_POP43_T42_Gaussian_bilinear.nc'
  #filename = 'rmp_T42_Gaussian_mask_POP43_idw.nc'
  #filename = 'rmp_POP43_T42_Gaussian_bilinear_old.nc'
  #filename = 'rmp_T42_Gaussian_POP43_idw.nc' 
  filename = 'rmp_gx1v1_T42_Gaussian_bilinear.nc'
  #filename = 'rmp_T42_Gaussian_Ocean_1v1_triplepole_bilinear.nc'
  #filename = 'rmp_Ocean_1v1_triplepole_T42_Gaussian_bilinear.nc'
  #filename = 'rmp_T42_Gaussian_mask_POP43_bilinear.nc'
  #filename = 'rmp_T42_Gaussian_Gamil_128x60_Grid_bilinear.nc' 
  #filename = 'rmp_T42_Gaussian_mask_POP43_idw.nc' 
  #filename = 'rmp_ll1deg_grid_licom_eq1x1_degree_Grid_bilinear.nc' 
  #filename = 'rmp_Ocean_1v1_triplepole_T42_Gaussian_bilinear.nc'
  #filename = 'rmp_T42_Gaussian_Ocean_1v1_triplepole_bilinear.nc'
  #filename = 'rmp_POP43_T42_Gaussian_idw_nearest3.nc'
  #filename = 'rmp_T42_Gaussian_POP43_bilinear.nc'
  #filename = 'rmp_T42_Gaussian_POP43_bilinear.nc' 
  #filename = 'rmp_T42_Gaussian_mask_POP43_bilinear.nc' 
  #filename = 'rmp_atmos_fv_0_POP43_bilinear.nc'
  #filename = 'rmp_atmos_grid_SCRIPTS_0_POP43_bilinear.nc'
  #filename = 'rmp_POP43_atmos_grid_SCRIPTS_0_bilinear.nc'
  #filename = 'rmp_Ocean_1v1_for_SCRIP_POP43_bilinear.nc'
  [src_coords_lat, src_coords_lon, dst_coords_lat, dst_coords_lon, remap_src_indx, remap_dst_indx, remap_matrix_compact] = load_rmpwfile(filename)
  dst_data = []
  for i in range(max(remap_dst_indx) + 1):
    dst_data.append(0.0)
  for i in range(len(remap_matrix_compact)):
    lat = src_coords_lat[remap_src_indx[i]] * math.pi / 180
    lon = src_coords_lon[remap_src_indx[i]] * math.pi / 180
    dst_data[remap_dst_indx[i]] += remap_matrix_compact[i] * test_func3(lat, lon)
    #if remap_dst_indx[i] == 1556:
    #  print 'begin'
    #  print src_coords_lat[remap_src_indx[i]]
    #  print src_coords_lon[remap_src_indx[i]]
    #  print test_func1(lat, lon)
    #  print test_func1(-54.41619931860472 * math.pi / 180, 56.25 * math.pi / 180)
    #  print remap_matrix_compact[i]
    #  print dst_data[1556]
    #  print 'end'

    #print remap_dst_indx[i]
    #print remap_matrix_compact[i]
    #print test_func1(lat, lon)
    #print dst_data[remap_dst_indx[i]]
    #print ''
    #if dst_data[remap_dst_indx[i]] > 3:
    #  print 'bug'
    #  print i
  
  cnt = 0
  err_acc = 0.0
  max_err = 0.0
  rmse = 0.0
  i = 0
  print len(dst_data)
  for item in dst_data:
    if item:
      lat = dst_coords_lat[i] * math.pi / 180
      lon = dst_coords_lon[i] * math.pi / 180
      real = test_func3(lat, lon)
      r_err = abs(real - item) / real
      rmse += (real - item) **2
      if r_err > 0.02:
        print i
        print dst_coords_lat[i] 
        print dst_coords_lon[i]
        print item
        print real
        print r_err
        print ''
      err_acc += r_err
      if r_err > max_err:
        max_err = r_err
      cnt += 1
    i += 1
  
  avg_err = err_acc / cnt
  rmse = rmse / (cnt - 1)

  print 'cnt', cnt
  print 'average relative error is', avg_err
  print 'max relative error is', max_err
  print 'rmse is', rmse
  
