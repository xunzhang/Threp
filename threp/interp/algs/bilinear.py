#! /usr/bin/python
# Filename: bilinear.py

''''''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import threp_import
from bilinearbox import Bilinearbox
from interp import Interp
from bilinear_solver import Bilinear_Solver
from bilinear_predictor import Bilinear_Predictor
from collineation import check_collineation
from selectrect import is_convex_quadrangle 
from idw_solver import Idw_Solver
from writenc import Writenc

class Bilinear(Interp):
  
  def __init__(self, src_grid_file_name, dst_grid_file_name):
    Interp.__init__(self, src_grid_file_name, dst_grid_file_name) 
    self.bilinearbox_obj = Bilinearbox(self.stree_base_obj, self.stree)
  
  def check_triangle(self, box):
    for i in range(4):
      for j in range(i + 1, 4):
        for k in range(j + 1, 4):
          if check_collineation(box[i], box[j], box[k]):
            return True
    return False
    
  def switch(self, rect_box):
    cross_pdt_h = (rect_box[0][0] - rect_box[1][0]) * (rect_box[3][1] - rect_box[2][1]) - (rect_box[0][1] - rect_box[1][1]) * (rect_box[3][0] - rect_box[2][0])
    cross_pdt_v = (rect_box[1][0] - rect_box[2][0]) * (rect_box[0][1] - rect_box[3][1]) - (rect_box[1][1] - rect_box[2][1]) * (rect_box[0][0] - rect_box[3][0])
    if cross_pdt_h != 0 and cross_pdt_v != 0:
      return 1
    elif cross_pdt_h == 0 and cross_pdt_v == 0:
      return 3
    elif cross_pdt_h == 0:
      return 2
    else:
      return 1
  
  # interp process in Bilinear subclass.
  def interp(self):
    #print self.dst_grid_center_lon[0]
    #print self.dst_grid_center_lat[0]
    #point = (self.dst_grid_center_lon[0], self.dst_grid_center_lat[0])
    #point = (0.0, 0.0)
    n = len(self.dst_grid_center_lon)
    for i in range(n):
      # ignore masked pnt
      if self.dst_grid_imask[i] == 0:
        print 'My mask is zero!'
        self.remap_matrix.append([])
        self.remap_matrix_indx.append([])
        continue
      
      # debug recovery function
      #dst_point = (357.625, -82.375)
      dst_point = (self.dst_grid_center_lon[i], self.dst_grid_center_lat[i])
      indx, lst = self.bilinearbox_obj.find_nearest_k(dst_point, 4)
      # suppose atom grid has no mask
      # case ocn2atm, a atm cell with a land cell below
      if Interp.check_all_masks(self, indx, 4):
        print 'It must be a land cell.'
        self.remap_matrix.append([])
        self.remap_matrix_indx.append([])
        continue
      # decide if dst pnt is coincide with a src pnt
      local_wgt = []
      if dst_point in lst:
        print 'coincide'
        for item in lst:
          if item == dst_point:
            local_wgt.append(1.0)
          else:
            local_wgt.append(0.0)
        # set remap_matrix and remap_matrix_indx objs
        self.remap_matrix.append(local_wgt)
        indx = Interp.indx_recovery(self, indx)
        self.remap_matrix_indx.append(indx)
        continue
      # find a bilinear box
      outside_flag, full_flag, bilinear_box_indx, bilinear_box = self.bilinearbox_obj.find_nearest_box(dst_point)
      
      # can not find 4 cells with no masks
      # use idw algorithm instead
      if not full_flag:
        bilinear_solver= Idw_Solver(dst_point, bilinear_box)
        bilinear_solver.solve()
        bilinear_box_indx = Interp.indx_recovery(self, bilinear_box_indx)
        self.remap_matrix.append(bilinear_solver.wgt_lst)
        self.remap_matrix_indx.append(bilinear_box_indx)
        continue
        
      # if can not be contained or bounding rect is a triangle
      # deciding a triangle by checking if three of them is collinearion
      if outside_flag or self.check_triangle(bilinear_box):
        print 'predictor case.'
        bilinear_solver = Bilinear_Predictor(dst_point, bilinear_box)
        bilinear_solver.predict() 
        # print debug info in detail
        if outside_flag:
          print 'outside'
          if not is_convex_quadrangle(bilinear_box):
            print 'it is a non-convex quadrangle, so it must be outside.'
          else:
            print 'trully meaning extrapolation.' 
        else:
          print 'it is a bounding triangle box.'
      else:
        print dst_point  
        print bilinear_box
        print 'normal case'
        bilinear_solver = Bilinear_Solver(dst_point, bilinear_box) 
        branch = self.switch(bilinear_box)
        if branch == 1:
          bilinear_solver.solve_bilinear_case1()
        if branch == 2:
          bilinear_solver.solve_bilinear_case2()
        if branch == 3: 
          bilinear_solver.solve_bilinear_case3()

      # transferm ghost bilinear_box_indx to original
      bilinear_box_indx = Interp.indx_recovery(self, bilinear_box_indx)
      
      print dst_point
      print bilinear_box
      print bilinear_box_indx
      print bilinear_solver.wgt_lst
      print ''

      # store result into objs
      #self.interp_wgt = bilinear_solver.wgt_lst
      #self.interp_box_indx = bilinear_box_indx
      #self.interp_box = bilinear_box
       
      # set remap_matrix and remap_matrix_indx objs 
      self.remap_matrix.append(bilinear_solver.wgt_lst)
      self.remap_matrix_indx.append(bilinear_box_indx)
    
    print 'remap_matrix size is:'
    print len(self.remap_matrix)
    
    # compact remap matrix, gen remap_src_indx and remap_dst_indx
    print 'Compacting remap matrix...'
    Interp.compact_remap_matrix(self)
    print 'Compacting finished!'
            
  def gen_remap_matrix_file(self):
    filename = 'rmp_' + self.src_grid_name + '_' + self.dst_grid_name + '_bilinear' 
    write_handler = Writenc(filename, self, 'bilinear')
    write_handler.write() 
     
  def remap(self): 

if __name__ == '__main__':
  #test_obj = Bilinear('../../grid/ll1deg_grid.nc', '../../grid/ll1deg_grid.nc')
  #test_obj = Bilinear('../../../grid/POP43.nc', '../../../grid/ll1deg_grid.nc')
  #test_obj = Bilinear('../../grid/ll2.5deg_grid.nc', '../../grid/T42.nc')
  #test_obj = Bilinear('../../grid/ll1deg_grid.nc', '../../grid/ll2.5deg_grid.nc')
  #test_obj = Bilinear('../../grid/T42.nc', '../../grid/ll1deg_grid.nc')
  test_obj = Bilinear('../../../grid/masked_T42_Gaussian_POP43/T42_Gaussian_mask.nc', '../../../grid/masked_T42_Gaussian_POP43/POP43.nc')
  #test_obj = Bilinear('../../../grid/masked_T42_Gaussian_POP43/POP43.nc', '../../../grid/masked_T42_Gaussian_POP43/T42_Gaussian_mask.nc')
  test_obj.interp()
  test_obj.gen_remap_matrix_file()
  
