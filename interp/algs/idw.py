#! /usr/bin/python
# Filename: idw.py

''' '''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>'] 

import sys
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
  
  def select_k(self, indx, lst, k):
    num = 0
    a = []
    b = []
    for i in range(len(indx)):
      if self.src_grid_imask[indx[i]] == 0:
        continue
      a.append(indx[i])
      b.append(lst[i])
      num += 1
      if num == k:
        break
    if num < k:
      print 'Bugs!!!'
      sys.exit()
    return a, b
   
  # decide if it is land cell
  def check_all_masks(self, indx):
    checksum = 0
    for i in indx:
      if self.src_grid_imask[i] == 0:
        checksum += 1
    if checksum == 4:
      return True
    else:
      return False
    
  def find_neighbors(self, dst_point):
    indx, lst = self.idw_obj.find_nearest_k(dst_point, self.nearest_k * 2)
    if self.check_all_masks(indx[0:4]):
      indx = []
      lst = []
    else:
      indx, lst = self.select_k(indx, lst, self.nearest_k)
    return indx, lst
    
  def interp(self):
    n = len(self.dst_grid_center_lon)
    # travese each dst pnt
    for i in range(n):
      # ignore the masked point
      if self.dst_grid_imask[i] == 0:
        print 'My mask is zero!'
        continue
      dst_point = (self.dst_grid_center_lon[i], self.dst_grid_center_lat[i])
      #dst_point = (300.0, -83.75)
      #neighbor_indx, neighbor_lst = self.idw_obj.find_nearest_k(dst_point, self.nearest_k)
      neighbor_indx, neighbor_lst = self.find_neighbors(dst_point)
      
      idw_solver = Idw_Solver(dst_point, neighbor_lst, self.eps, self.power)
      idw_solver.solve()
      print dst_point
      print neighbor_lst
      print idw_solver.wgt_lst
      print ''

if __name__ == '__main__':
  #test_obj = Idw('../../grid/ll1deg_grid.nc', '../../grid/ll2.5deg_grid.nc', 4)
  test_obj = Idw('../../grid/T42.nc', '../../grid/ll1deg_grid.nc', 4)
  #test_obj = Idw('../../grid/POP43.nc', '../../grid/T42.nc', 4)
  test_obj.interp()
