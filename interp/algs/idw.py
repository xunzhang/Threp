#! /usr/bin/python
# Filename: idw.py

''' '''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>'] 

import threp_import
from nearest import Search
from interp import Interp
from idw_solver import Idw_Solver

class Idw(Interp):

  def __init__(self, src_grid_file_name, dst_grid_file_name, k):
    Interp.__init__(self, src_grid_file_name, dst_grid_file_name)
    self.power = 1
    self.eps = 1.0e-6
    self.nearest_k = k
    self.idw_obj = Search(self.stree_base_obj, self.stree)

  def interp(self):
    n = len(self.dst_grid_center_lon)
    # travese each dst pnt
    for i in range(2):
      dst_point = (self.dst_grid_center_lon[i], self.dst_grid_center_lat[i])
      neighbor_indx, neighbor_lst = self.idw_obj.find_nearest_k(dst_point, self.nearest_k)
      idw_solver = Idw_Solver(dst_point, neighbor_lst, self.eps, self.power)
      idw_solver.solve()
      print dst_point
      print neighbor_lst
      print idw_solver.wgt_lst
       

if __name__ == '__main__':
  test_obj = Idw('../../grid/T42.nc', '../../grid/POP43.nc', 4)
  test_obj.interp()
