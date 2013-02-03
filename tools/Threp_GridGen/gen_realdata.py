#! /usr/bin/python
# Filename: gen_realdata.py

import time
import scipy
from numpy import dtype
from Scientific.IO.NetCDF import NetCDFFile as Dataset

path = '../../grid/CPLDATA/'
file_lst = ['X02.cpl6.ha.0006-12.nc', 'X02.cpl6.ha.0007-04.nc', 'X02.cpl6.ha.0007-08.nc', 'X02.cpl6.ha.0007-01.nc', 'X02.cpl6.ha.0007-05.nc', 'X02.cpl6.ha.0007-09.nc', 'X02.cpl6.ha.0007-02.nc', 'X02.cpl6.ha.0007-06.nc', 'X02.cpl6.ha.0007-10.nc', 'X02.cpl6.ha.0007-03.nc', 'X02.cpl6.ha.0007-07.nc', 'X02.cpl6.ha.0007-11.nc']
var_lst = ['avXa2c_a_Sa_z', 'avXa2c_a_Sa_u', 'avXa2c_a_Sa_v', 'avXa2c_a_Sa_tbot', 'avXa2c_a_Sa_ptem', 'avXa2c_a_Sa_shum', 'avXa2c_a_Sa_dens', 'avXa2c_a_Sa_pbot', 'avXa2c_a_Sa_pslv', 'avXa2c_a_Sa_co2prog', 'avXa2c_a_Sa_co2diag', 'avXa2c_a_Faxa_lwdn', 'avXa2c_a_Faxa_rainc', 'avXa2c_a_Faxa_rainl', 'avXa2c_a_Faxa_snowc', 'avXa2c_a_Faxa_snowl', 'avXa2c_a_Faxa_swndr', 'avXa2c_a_Faxa_swvdr', 'avXa2c_a_Faxa_swndf', 'avXa2c_a_Faxa_swvdf', 'avXa2c_a_Faxa_swnet']

def gen_realdata(path, filename, var):
  ncfile = Dataset(path + filename, 'r')
  filename = './realdata/T42_' + var + '-' + filename.split('.')[-2] + '.nc'
  nc = Dataset(filename, 'w')
  tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
  nx = 128
  ny = 64
  grid_size = ncfile.dimensions['n_a']

  # load data
  data = ncfile.variables[var][:, :, :]
  long_name = ncfile.variables[var].long_name
  units = ncfile.variables[var].units
  missing_value = ncfile.variables[var].missing_value
  _FillValue = ncfile.variables[var]._FillValue
  cell_method = ncfile.variables[var].cell_method
  tmp = []
  for i in range(1):
    for j in range(ny):
      for k in range(nx):
        tmp.append(data[i][j][k])
  data = scipy.array(tmp)

  # create variables
  nc.createDimension('grid_size', nx * ny)

  # create varibels
  data_var = nc.createVariable('data', dtype('d').char, ('grid_size',))
  
  data_var[:] = data
  data_var.long_name = long_name
  data_var.units = units
  data_var.missing_value = missing_value
  data_var._FillValue = _FillValue
  data_var.cell_method = cell_method
 
  string = 'Threp' + var + ' data'
  setattr(nc, 'title', string)
  setattr(nc, 'createdata', tm)

  nc.close()
  ncfile.close()
  print '*** Successfully generating real data file. ***'

if __name__ == '__main__':
  for filename in file_lst:
    for var in var_lst:
      gen_realdata(path, filename, var)

