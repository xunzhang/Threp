#! /usr/bin/python
# Filename: idw.py

''' '''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>'] 

import sys
import threp_import
from nearest import Search
from interp import Interp
from idw_solver import Idw_Solver
from writenc import Writenc
from mpi4py import MPI

class Idw(Interp):
  
  # init Idw object.
  # init self.eps to avoid deviding by zero, init the search object self.idw_obj
  def __init__(self, src_grid_file_name, dst_grid_file_name, online_flag, realdata_file_name, k):
    Interp.__init__(self, src_grid_file_name, dst_grid_file_name, online_flag, realdata_file_name)
    self.power = 1
    self.eps = 1.0e-6
    self.nearest_k = k
    self.idw_obj = Search(self.stree_base_obj, self.stree)
  
  # local select in idw algorithm 
  # select nearest k no-mask-pnts in intermediate result
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
      #for i in indx:
      #  print self.src_grid_imask[i]
      print 'Not full k'
      #sys.exit()
    return a, b
  
  # calc k idw neighbors, sorted, with no mask 
  def find_idw_neighbors(self, dst_point):
    indx, lst = self.idw_obj.find_nearest_k(dst_point, self.nearest_k * 4)
    # there may be bugs.
    if Interp.check_all_masks(self, indx[0:self.nearest_k], self.nearest_k):
      indx = []
      lst = []
    else:
      indx, lst = self.select_k(indx, lst, self.nearest_k)
    return indx, lst
    
  # interp process in Idw subclass.
  def interp(self):
    n = len(self.dst_grid_center_lon)
    # traverse dst pnt
    for i in range(n):
      # ignore masked pnt
      if self.dst_grid_imask[i] == 0:
        print 'My mask is zero!'
        self.remap_matrix.append([])
        self.remap_matrix_indx.append([])
        continue

      dst_point = (self.dst_grid_center_lon[i], self.dst_grid_center_lat[i])
      neighbor_indx, neighbor_lst = self.find_idw_neighbors(dst_point)
      
      # suppose atm grid has no mask 
      # case ocn2atm, a atm cell with a land cell below
      if not neighbor_indx:
        print 'It must be a land cell.'
        self.remap_matrix.append([])
        self.remap_matrix_indx.append([])
        continue
      
      # normal case, init idw_solver 
      idw_solver = Idw_Solver(dst_point, neighbor_lst, self.eps, self.power)
      
      # decide if dst pnt is coincide with a src pnt
      if dst_point in neighbor_lst:
        print 'coincide'
        for item in neighbor_lst:
          if item == dst_point:
            idw_solver.wgt_lst.append(1.0)
          else:
            idw_solver.wgt_lst.append(0.0)
      else: 
        # solve normal case
        idw_solver.solve()
      
      print 'ss'
      print neighbor_indx 
      # transform ghost indx to original
      neighbor_indx = Interp.indx_recovery(self, neighbor_indx)
      print neighbor_indx 
      
      print ''
      print dst_point
      print neighbor_lst
      print neighbor_indx
      print idw_solver.wgt_lst

      # store result into objs
      #self.interp_wgt = idw_solver.wgt_lst
      #self.interp_box_indx = neighbor_indx
      #self.interp_box = neighbor_lst
  
      # set remap_matrix and remap_matrix_indx objs
      self.remap_matrix.append(idw_solver.wgt_lst)
      self.remap_matrix_indx.append(neighbor_indx)
      if len(idw_solver.wgt_lst) != len(neighbor_indx):
        print idw_solver.wgt_lst
        print neighbor_indx
        print 'ERRORRRR'
        sys.exit()

    print 'remap_matrix size is:'
    print len(self.remap_matrix)
   
    # compact remap matrix, gen remap_src_indx and remap_dst_indx
    #print 'Compacting remap matrix...'
    #Interp.compact_remap_matrix(self)
    #print 'Compacting finished!'

  def gen_remap_matrix_file(self):
    filename = 'rmp_' + self.src_grid_name + '_' + self.dst_grid_name + '_idw.nc'
    write_handler = Writenc(filename, self, 'idw')
    write_handler.write()
  
  def remap(self):
    remap_result = Interp.remap(self)
    return remap_result
   
if __name__ == '__main__':
  comm = MPI.COMM_WORLD
  size = comm.Get_size()
  rank = comm.Get_rank()
  #test_obj = Idw('../../grid/ll2.5deg_grid.nc', '../../grid/ll2.5deg_grid.nc', 4)
  #test_obj = Idw('../../grid/ll1deg_grid.nc', '../../grid/ll2.5deg_grid.nc', 4)
  #test_obj = Idw('../../grid/T42.nc', '../../grid/ll1deg_grid.nc', 4)
  #test_obj = Idw('../../../grid/POP43.nc', '../../../grid/ll1deg_grid.nc', 4)
  #test_obj = Idw('../../grid/POP43.nc', '../../grid/T42.nc', 4)
  #test_obj = Idw('../../grid/T42.nc', '../../grid/POP43.nc', 4)
  #test_obj = Idw('../../../grid/masked_T42_Gaussian_POP43/T42_Gaussian_mask.nc', '../../../grid/masked_T42_Gaussian_POP43/POP43.nc', True, '../../../data/real/T42_Gaussian_Grid/T42_avXa2c_a_Faxa_lwdn-0006-12.nc', 4)
  #test_obj = Idw('../../../grid/T42_Gaussian_POP43/T42_Gaussian.nc', '../../../grid/T42_Gaussian_POP43/POP43.nc', True, '../../../data/real/T42_Gaussian_Grid/T42_avXa2c_a_Faxa_lwdn-0006-12.nc', 4)
  test_obj = Idw('../../../grid/T42_Gaussian_POP43/POP43.nc', '../../../grid/T42_Gaussian_POP43/T42_Gaussian.nc', False, '../../../data/real/T42_Gaussian_Grid/T42_avXa2c_a_Faxa_lwdn-0007-08.nc', 4)
  test_obj.dst_distribute(rank, size)
  test_obj.interp()
  if rank == 0:
    # compact remap matrix, gen remap_src_indx and remap_dst_indx
    print 'Compacting remap matrix...'
    Interp.compact_remap_matrix(test_obj)
    print 'Compacting finished!'
    test_obj.gen_remap_matrix_file()
    remap_result = test_obj.remap()
    print remap_result
   
