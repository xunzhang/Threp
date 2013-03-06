#! /usr/bin/python
# Filename: remap_entry.py

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import threp_import
import bilinear
from interp import Interp
from mpi4py import MPI

def remap_entry(src_file, dst_file, alg_name, real_data_file, offline_flag, rank, size, comm):
  if offline_flag:
    test_obj = alg_name(src_file, dst_file, False, real_data_file)
  else:
    test_obj = alg_name(src_file, dst_file, True, real_data_file)
  test_obj.dst_distribute(rank, size)
  test_obj.interp()
  test_obj.dst_merge(rank, comm)
  if rank == 0:
    Interp.compact_remap_matrix(test_obj)
    if offline_flag:
      test_obj.gen_remap_matrix_file()
    else:
      #test_obj.gen_remap_matrix_file()
      remap_result = test_obj.remap()
      print remap_result

if __name__ == '__main__':
  comm = MPI.COMM_WORLD
  size = comm.Get_size()
  rank = comm.Get_rank()
  remap_entry('../../grid/T42_Gaussian_POP43/POP43.nc', '../../grid/T42_Gaussian_POP43/T42_Gaussian.nc', bilinear.Bilinear, 'null', True, rank, size, comm)
  
