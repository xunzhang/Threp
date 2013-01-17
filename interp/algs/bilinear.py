#! /usr/bin/python
# Filename: bilinear.py

''''''

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

#import sys
#sys.path.append("../../search/")
#sys.path.append("../")
import threp_import
from bilinearbox import Bilinearbox
from interp import Interp

class Bilinear(Interp):
  
  def __init__(self, src_grid_file_name, dst_grid_file_name):
    Interp.__init__(self, src_grid_file_name, dst_grid_file_name) 
    self.bilinearbox_obj = Bilinearbox(self.stree_base_obj, self.stree)
    
  def interp(self):
    print self.dst_grid_center_lon[0]
    print self.dst_grid_center_lat[0]
    test_point = (self.dst_grid_center_lon[0], self.dst_grid_center_lat[0])
    self.bilinearbox_obj.find_nearest_box(test_point)
    #for i in range(len(self.dst_grid_center_lat)):
    #  self.bilinearbox_obj.find_nearest_box(())
    
  #def remap(self): 

if __name__ == '__main__':
  test_obj = Bilinear('../../grid/T42.nc', '../../grid/POP43.nc')
  test_obj.interp()
  
