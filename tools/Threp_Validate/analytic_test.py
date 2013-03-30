#! /usr/bin/python
# Filename: analytic_test.py

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import math
from Scientific.IO.NetCDF import NetCDFFile as Dataset
from genncfile import Genncfile

# 2 + cos(pi * r / L), 2 + cos(acos(-cos(lat) * cos(lon)) / 2)
def test_func1(lat, lon):
  val_tmp = -math.cos(lat) * math.cos(lon)
  return 2 + math.cos(math.acos(val_tmp) / 2) 

# 2 + cos(lat)^2 * sin(2lon)
def test_func2(lat, lon):
  return 2 + math.cos(lat) ** 2 * math.sin(2 * lon) 

# 2 + sin(2lat)^16 * cos(16lon)
def test_func3(lat, lon):
  return 2 + math.sin(2 * lat) ** 16 * math.cos(16 * lon)

class nchandler(Exception):

  def __init__(self, grid_size, lat, lon, phy, srcname, dstname, what, algname):
    self.grid_size = grid_size
    self.grid_center_lat = lat
    self.grid_center_lon = lon
    self.physical_variable = phy
    self.src_grid_name = srcname
    self.dst_grid_name = dstname
    self.name = what + '_' + srcname + '2' + dstname + '.nc'
    self.algname = algname

  def gen(self):
    nc = Genncfile(self.name, self, self.algname)
    nc.gen()
  
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

def parse(name):
  st = name.strip('.nc')
  algname = st.split('_')[-1]
  srcname = 'T42_Gaussian'
  dstname =  'Gamil_128x60_Grid'
  return srcname, dstname, algname
  
if __name__ == '__main__':
  filename = 'rmp_T42_Gaussian_Gamil_128x60_Grid_bilinear.nc'
  srcname, dstname, algname = parse(filename)
  [src_coords_lat, src_coords_lon, dst_coords_lat, dst_coords_lon, remap_src_indx, remap_dst_indx, remap_matrix_compact] = load_rmpwfile(filename)
  dst_data = []
  for i in xrange(max(remap_dst_indx) + 1):
    dst_data.append(0.0)
  for i in xrange(len(remap_matrix_compact)):
    lat = src_coords_lat[remap_src_indx[i]] * math.pi / 180
    lon = src_coords_lon[remap_src_indx[i]] * math.pi / 180
    dst_data[remap_dst_indx[i]] += remap_matrix_compact[i] * test_func1(lat, lon)
  
  i = 0
  lat_lst = []
  lon_lst = []
  real_lst = []
  item_lst = []
  diff_lst = []
  for item in dst_data:
    lat_lst.append(dst_coords_lat[i])
    lon_lst.append(dst_coords_lon[i] - 180.0)
    if item:
      lat = dst_coords_lat[i] * math.pi / 180
      lon = dst_coords_lon[i] * math.pi / 180
      real = test_func1(lat, lon)
      if dst_coords_lon[i] == 177.1875:#,180:#0:#357.1875:
        print real
      r_err = abs(real - item) / real
      real_lst.append(real)
      item_lst.append(item)
      diff_lst.append(r_err)
      if r_err < -1.0:
        print r_err
    else:
      real_lst.append(0.0)
      item_lst.append(0.0)
      diff_lst.append(0.0) 
    i += 1
  print len(real_lst)
  print len(dst_data)
  print len(item_lst)
  print len(diff_lst)
  print len(lat_lst)
  print len(lon_lst) 
  realdata_obj = nchandler(len(dst_data), lat_lst, lon_lst, real_lst, srcname, dstname, 'real', algname)
  remapdata_obj = nchandler(len(dst_data), lat_lst, lon_lst, item_lst, srcname, dstname, 'remap', algname)
  errordata_obj = nchandler(len(dst_data), lat_lst, lon_lst, diff_lst, srcname, dstname, 'error', algname)
  realdata_obj.gen()
  remapdata_obj.gen()
  errordata_obj.gen()
