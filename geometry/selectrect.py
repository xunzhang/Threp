#! /usr/bin/python
# Filename: selectrect.py

''' '''

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import sys
import copy
from planar import Polygon
from planar import Point
from clockwise_sort import clockwise_sort

#from matplotlib.path import Path
#from shapely.geometry import Polygon
#from shapely.geometry import Point

#Path([[0, 1], [1, 1], [1, 0], [0, 0]]).contains_point([0.5, 0.5])
#def is_contain(query_point, vertex_lst):
#  cond = Path(vertex_lst).contains_point(query_point) or query_point in vertex_lst
#  if cond:
#    return True
#  else:
#    return False 

#def is_contain(query_point, vertex_lst):
#  polygon = Polygon(tuple(vertex_lst))
#  point = Point(query_point)
#  return polygon.contains(point)

def is_convex_quadrangle(box):
  polygon = Polygon(box)
  return polygon.is_convex

def is_contain(query_point, vertex_lst):
  if len(vertex_lst) == 4:
    vertex_box = copy.deepcopy(vertex_lst)
    vertex_box = clockwise_sort(vertex_box)
    polygon = Polygon(vertex_box)
  else:
    polygon = Polygon(vertex_lst)
  point = Point(query_point[0], query_point[1])
  if not polygon.is_convex:
    return False
  return polygon.contains_point(point)

def select_containing_rect(pnt, neighbor_indx, neighbor_lst):
  pnt_num = len(neighbor_lst)
  if pnt_num > 16:
    print 'Bug!!'
    sys.exit(), 
  # pnt_num must be less than 16, i < j < k
  for i in range(pnt_num):
    for j in range(i + 1, pnt_num):
      for k in range(j + 1, pnt_num):
        triangle = [neighbor_lst[i], neighbor_lst[j], neighbor_lst[k]]
        if is_contain(pnt, triangle):
          for l in range(k + 1, pnt_num):
            rect = copy.deepcopy(triangle)
            rect.append(neighbor_lst[l])
            if is_contain(pnt, rect):
              return False, [neighbor_indx[i], neighbor_indx[j], neighbor_indx[k], neighbor_indx[l]], rect
  return True, neighbor_indx[0:4], neighbor_lst[0:4]
        
