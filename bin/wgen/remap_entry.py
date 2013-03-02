#! /usr/bin/python
# Filename: remap_entry.py

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import threp_import
import bilinear

def remap_entry(src_file, dst_file, alg_name, real_data_file, offline_flag):
  if offline_flag:
    test_obj = alg_name(src_file, dst_file, False, real_data_file)
  else:
    test_obj = alg_name(src_file, dst_file, True, real_data_file)
  test_obj.interp()
  if offline_flag:
    test_obj.gen_remap_matrix_file()
  else:
    remap_result = test_obj.remap()
    print remap_result

if __name__ == '__main__':
  remap_entry('../../grid/T42_Gaussian_POP43/POP43.nc', '../../grid/T42_Gaussian_POP43/T42_Gaussian.nc', bilinear.Bilinear, 'null', offline_flag = True)
  
