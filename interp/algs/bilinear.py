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
      return 1
    else:
      return 2
   
  # tackle mask problem 
  def interp(self):
    #print self.dst_grid_center_lon[0]
    #print self.dst_grid_center_lat[0]
    #point = (self.dst_grid_center_lon[0], self.dst_grid_center_lat[0])
    #point = (0.0, 0.0)
    
    n = len(self.dst_grid_center_lon)
    for i in range(n):
      # if dst point's mask is 0, no need to calc
      if self.dst_grid_imask[i] == 0:
        print 'My mask is zero!'
        continue
      
      dst_point = (self.dst_grid_center_lon[i], self.dst_grid_center_lat[i])
      # debug recovery function
      #dst_point = (357.625, -82.375)
      
      # For example, ocn2atm, check if it is a land underlying surface with a atm cell.
      indx, lst = self.bilinearbox_obj.find_nearest_k(dst_point, 4)
      if Interp.check_all_masks(self, indx, 4):
        print 'It must be a land cell.'
        continue
      
      # find a bilinear box
      outside_flag, bilinear_box_indx, bilinear_box = self.bilinearbox_obj.find_nearest_box(dst_point)
      
      # check if the dst_point is just a point in src grid.
      # if coincide with a src point, it must be the first search result(that's why after find a bilinear box)
      if dst_point in bilinear_box:
        print 'coincide'
        # set 4 wgts as [1, 0, 0, 0]
        self.interp_wgt = [1.0, 0.0, 0.0, 0.0]
        continue
      # if can not be contained and bounding rect is a triangle
      # deciding a triangle by checking if three of them is collinearion
      if outside_flag or self.check_triangle(bilinear_box):
        print 'predictor case.'
        bilinear_solver = Bilinear_Predictor(dst_point, bilinear_box)
        bilinear_solver.predict() 
        if outside_flag:
          print 'outside'
          # non-convex quadrangle case
          if not is_convex_quadrangle(bilinear_box):
            print 'it is a non-convex quadrangle.'
        # else it is a triangle box.
        else:
          print 'it is a bounding triangle.'
        print bilinear_solver.wgt_lst
      else:
        print 'normal case'
        bilinear_solver = Bilinear_Solver(dst_point, bilinear_box)        
        branch = self.switch(bilinear_box)
        if branch == 1:
          bilinear_solver.solve_bilinear_case1()
        if branch == 2:
          bilinear_solver.solve_bilinear_case2()
        if branch == 3: 
          bilinear_solver.solve_bilinear_case3()
            
        print bilinear_solver.wgt_lst

      # transfer ghost bilinear_box_indx
      bilinear_box_indx = Interp.indx_recovery(self, bilinear_box_indx)
      
      # store result into objs
      self.interp_wgt = bilinear_solver.wgt_lst
      self.interp_box_indx = bilinear_box_indx
      self.interp_box = bilinear_box
       
      print dst_point
      print bilinear_box_indx
      print bilinear_box
      print ''
    
  #def remap(self): 

if __name__ == '__main__':
  test_obj = Bilinear('../../grid/ll1deg_grid.nc', '../../grid/ll1deg_grid.nc')
  #test_obj = Bilinear('../../grid/ll2.5deg_grid.nc', '../../grid/ll1deg_grid.nc')
  #test_obj = Bilinear('../../grid/ll1deg_grid.nc', '../../grid/ll2.5deg_grid.nc')
  #test_obj = Bilinear('../../grid/T42.nc', '../../grid/ll1deg_grid.nc')
  test_obj.interp()
     
