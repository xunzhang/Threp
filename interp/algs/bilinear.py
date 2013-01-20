#! /usr/bin/python
# Filename: bilinear.py

''''''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import threp_import
from bilinearbox import Bilinearbox
from interp import Interp
from bilinear_solver import Bilinear_Solver
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
  
  # tackle mask problem 
  def interp(self):
    #print self.dst_grid_center_lon[0]
    #print self.dst_grid_center_lat[0]
    #point = (self.dst_grid_center_lon[0], self.dst_grid_center_lat[0])
    #point = (0.0, 0.0)
    
    n = len(self.dst_grid_center_lon)
    for i in range(n):
      if self.dst_grid_imask[i] == 0:
        print 'My mask is zero!'
        continue
      dst_point = (self.dst_grid_center_lon[i], self.dst_grid_center_lat[i])
      indx, lst = self.bilinearbox_obj.find_nearest_k(dst_point, 4)
      if Interp.check_all_masks(self, indx, 4):
        print 'It must be a land cell.'
        continue
      outside_flag, bilinear_box_indx, bilinear_box = self.bilinearbox_obj.find_nearest_box(dst_point)
      print outside_flag
      if outside_flag:
        print 'it is reget'  
      else:
        # check if three of them is collineation
        if self.check_triangle(bilinear_box):
          print 'it is a bounding triangle.'
        # it is a non-convex quadrangle
        elif not is_convex_quadrangle(bilinear_box):
          print 'it is a non-convex quadrangle'
        else:
          print 'normal case'
          bilinear_solver = Bilinear_Solver(dst_point, bilinear_box)
          bilinear_solver.regular_solve()
      print dst_point
      print bilinear_box_indx
      print bilinear_box
      print ''
    
  #def remap(self): 

if __name__ == '__main__':
  test_obj = Bilinear('../../grid/ll2.5deg_grid.nc', '../../grid/ll1deg_grid.nc')
  #test_obj = Bilinear('../../grid/ll1deg_grid.nc', '../../grid/ll2.5deg_grid.nc')
  test_obj.interp()
    
