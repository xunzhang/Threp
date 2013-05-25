#! /usr/bin/python
# Filename: interp.py

import copy
import sys
import threp_import
from loadnc import Loadnc
from loadreal import Loadreal
from build import Build

class Interp(Exception):
  
  def __init__(self, src_grid_file_name, dst_grid_file_name, online_flag, src_realdata_file_name):
    src_nc_obj = Loadnc(src_grid_file_name)
    self.src_grid_size, self.src_grid_corners, self.src_grid_rank, self.src_grid_dims, self.src_grid_center_lat, self.src_grid_center_lon, self.src_grid_imask = src_nc_obj.load()
    src_nc_obj.closenc()
    
    # set south pole pnts
    pole_num = 0
    self.pole_south = []
    self.pole_south_indx = []
    for i in xrange(len(self.src_grid_center_lat)):
      if self.src_grid_imask[i] == 1:
        self.pole_south.append((self.src_grid_center_lon[i], self.src_grid_center_lat[i]))
        self.pole_south_indx.append(i)
        pole_num += 1
      if pole_num == 10:
        break  
    self.pole_south_bnd = min([item[1] for item in self.pole_south])
    # set north pole pnts
    pole_num = 0
    self.pole_north = []
    self.pole_north_indx = []
    j = len(self.src_grid_center_lat)
    #while True:
    while 1:
      j -= 1
      if self.src_grid_imask[j] == 1:
        self.pole_north.append((self.src_grid_center_lon[j], self.src_grid_center_lat[j]))
        self.pole_north_indx.append(j)
        pole_num += 1
      if pole_num == 10:
        break
    self.pole_north_bnd = max([item[1] for item in self.pole_north])

    # original grid info
    # used for remap matrix file
    self.original_src_grid_center_lat = copy.deepcopy(self.src_grid_center_lat)
    self.original_src_grid_center_lon = copy.deepcopy(self.src_grid_center_lon)
    self.original_src_grid_imask = copy.deepcopy(self.src_grid_imask)
     
    dst_nc_obj = Loadnc(dst_grid_file_name)
    self.dst_grid_size, self.dst_grid_corners, self.dst_grid_rank, self.dst_grid_dims, self.dst_grid_center_lat, self.dst_grid_center_lon, self.dst_grid_imask = dst_nc_obj.load()
    dst_nc_obj.closenc()
    
    self.stree_base_obj = Build(self.src_grid_size, self.src_grid_corners, self.src_grid_rank, self.src_grid_dims, self.src_grid_center_lat, self.src_grid_center_lon, self.src_grid_imask)
    self.recovery_indx_table, self.stree = self.stree_base_obj.grow()
    
    self.src_grid_name = src_grid_file_name.split('/')[-1].split('.')[0]
    self.dst_grid_name = dst_grid_file_name.split('/')[-1].split('.')[0]
     
    #self.interp_wgt = []
    #self.interp_box_indx = []
    #self.interp_box = []
    self.remap_matrix = []
    self.remap_matrix_indx = []
    
    self.remap_matrix_compact = []
    self.remap_src_indx = []
    self.remap_dst_indx = []
    
    # load real data if online remapping
    # self.src_data = []
    if online_flag:
      src_data_nc_obj = Loadreal(src_realdata_file_name)
      size, self.src_data = src_data_nc_obj.load()
      if size != self.src_grid_size:
        print 'Real data size does not match grid size.'
        sys.exit()
      src_data_nc_obj.closenc()
    
    self.dst_data = [] 
  
  # for mpi use
  def dst_distribute(self, rank, size):
    # load balance, grid size reps load
    load_sum = self.dst_grid_size
    load = load_sum / size
    if load_sum % size:
      if rank == size - 1:
        load = load_sum - load * (size - 1)
    # dst_grid_dims dst_grid_size is changed in mpi case, but no place using it, so let it be..
    # self.dst_grid_dims = self.dst_grid_dims
    # self.dst_grid_size = load
    start_indx = (load_sum / size) * rank
    self.dst_grid_center_lat = self.dst_grid_center_lat[start_indx : start_indx + load] 
    self.dst_grid_center_lon = self.dst_grid_center_lon[start_indx : start_indx + load]
    self.dst_grid_imask = self.dst_grid_imask[start_indx : start_indx + load] 
  
  # for mpi use
  def dst_merge(self, rank, comm):
    self.remap_matrix = comm.gather(self.remap_matrix, root = 0)
    self.remap_matrix_indx = comm.gather(self.remap_matrix_indx, root = 0)
    self.dst_grid_center_lat = comm.gather(self.dst_grid_center_lat, root = 0)
    self.dst_grid_center_lon = comm.gather(self.dst_grid_center_lon, root = 0)
    self.dst_grid_imask = comm.gather(self.dst_grid_imask, root = 0)
    if rank == 0:
      self.remap_matrix = [val for item in self.remap_matrix for val in item] 
      self.remap_matrix_indx = [val for item in self.remap_matrix_indx for val in item]
      self.dst_grid_center_lat = [val for item in self.dst_grid_center_lat for val in item]
      self.dst_grid_center_lon = [val for item in self.dst_grid_center_lon for val in item]
      self.dst_grid_imask = [val for item in self.dst_grid_imask for val in item]

  def check_wgt(self, wgt):
    for item in wgt:
      if item > 2 or item < -2:
        print item
        print 'wgt is invalid'
        sys.exit()
  
  def check_wgtsum(self, wgt):
    lsum = 0.0
    for item in wgt:
      lsum += item
    if abs(lsum - 1.0) > 0.3:
      print lsum
      print 'sum of local wgts is invalid'
      sys.exit()
  
  # decide if all indx cells are masked out
  def check_all_masks(self, indx, n):
    checksum = 0
    for i in indx:
      if self.src_grid_imask[i] == 0:
        checksum += 1
    if checksum == n:
      return True
    else:
      return False
  
  def indx_recovery(self, indx_lst):
    tmp_indx = [] 
    for i in indx_lst:
      if i >= self.src_grid_size:
        print 'recovery ghost index.'
        tmp_indx.append(self.recovery_indx_table[i])
      else:
        tmp_indx.append(i)
    indx_lst = tmp_indx
    return indx_lst

  def indx_lrec_recovery(self, indx_lst):
    tmp_indx = []
    for i in indx_lst:
      if i >= self.src_grid_size:
        flag = True
        print 'recovery ghost index.'
        if (i / self.src_grid_dims[1]) == 1:
          offset = 0
        else:
          offset = self.src_grid_dims[0] - 1
        tmp_indx.append((i % self.src_grid_dims[1]) * self.src_grid_dims[0] + offset)
      else:
        tmp_indx.append(i)
    indx_lst = tmp_indx
    return indx_lst
      
  # virtual function to do calc wgts  
  def interp(self):
    pass
     
  def compact_remap_matrix(self):
    i = 0
    k = 0
    for matrix_item in self.remap_matrix:
      if matrix_item:
        j = 0
        for wgt in matrix_item:
          self.remap_matrix_compact.append(wgt)
          self.remap_src_indx.append(self.remap_matrix_indx[i][j])
          self.remap_dst_indx.append(k)
          j += 1
      #else:
      #  self.remap_dst_indx.append(k)
      k += 1
      i += 1  
    
  # virtual function to interpolate data 
  def remap(self):
    # init dst_data list as 0.0
    print max(self.remap_dst_indx)
    for i in xrange(max(self.remap_dst_indx) + 1):
      self.dst_data.append(0.0)
    # interpolate    
    for i in xrange(len(self.remap_matrix_compact)):
      self.dst_data[self.remap_dst_indx[i]] += self.remap_matrix_compact[i] * self.src_data[self.remap_src_indx[i]]
    return self.dst_data

  # for mpi use
  # parallelize with rows
  # rank 0 measure load of remapping step
  # only rank 0 needs to exec 
  # [1, 1, 1, 2, 2, 2, 2, 4, 4, 5, 5, 5, 5, 6, 6, 6] -> [0:3], [3:7], [7:9], [9, 13], [13:16] -> [0, 3, 7, 9, 13, 16]
  def learn(self, size):
    tmp = list(set(self.remap_dst_indx))
    learn_lst = [0]
    load_sum = len(tmp)
    load = load_sum / size
    if load_sum % size:
      last_load = load_sum - load * (size - 1)
    else:
      last_load = load
    j = 0
    cnt = 1
    rank_cnt = 0
    for i in xrange(len(self.remap_dst_indx)):
      if self.remap_dst_indx[i] != tmp[j]:
        if cnt == load:
          if rank_cnt == size - 1:
            break
          rank_cnt += 1
          learn_lst.append(i)
          cnt = 0
        cnt += 1
        j += 1
    learn_lst.append(len(self.remap_dst_indx))
    return learn_lst
    
  # for mpi use
  # only rank 0 needs to exec
  # [0, 3, 7, 9, 16] -> [0:3] to rank 0
  #                  -> [3:7] to rank 1
  #                  -> [7:9] to rank 2
  #                  -> [9:16] to rank 3
  def deliver(self, deliver_disp, rank, size, comm):
    if rank == 0:
      for i in xrange(1, size):
        buf1 = self.remap_dst_indx[deliver_disp[i] : deliver_disp[i + 1]]
        buf2 = self.remap_src_indx[deliver_disp[i] : deliver_disp[i + 1]]
        buf3 = self.remap_matrix_compact[deliver_disp[i] : deliver_disp[i + 1]]
        comm.send(buf1, dest = i, tag = i)
        comm.send(buf2, dest = i, tag = 2 * i + 1)
        comm.send(buf3, dest = i, tag = 3 * i + 1)
      self.remap_dst_indx = self.remap_dst_indx[deliver_disp[0] : delive_disp[1]]
      self.remap_src_indx = self.remap_src_indx[deliver_disp[0] : delive_disp[1]]
      self.remap_matrix_compact = self.remap_matrix_compact[deliver_disp[0] : delive_disp[1]]
    else:
      self.remap_dst_indx = comm.recv(source = 0, tag = rank)
      self.remap_src_indx = comm.recv(source = 0, tag = 2 * rank + 1)
      self.remap_matrix_compact = comm.recv(source = 0, tag = 3 * rank + 1)
  
