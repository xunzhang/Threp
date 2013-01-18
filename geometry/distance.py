#! /usr/bin/python
# Filename: distance.py

''' '''

__author__ = ['Wu Hong<xunzhangthu@gmail.com>']

import math

def euc_dist(pt1, pt2):
  return math.sqrt( (pt2[0] - pt1[0] ) **2 + (pt2[1] - pt1[1]) **2 )
  
# pt: (lon, lat)
# cos-1(cos(dst_lat) * cos(src_lat) * (cos(dst_lon) * cos(src_lon) + sin(dst_lon) * sin(dst_lon)) + sin(dst_lat) * sin(src_lat))     
# see SCRIP1.4 user guide.
def sph_dist(pt1, pt2):
  return math.acos(math.cos(pt2[1]) * math.cos(pt1[1]) * (math.cos(pt2[0]) * math.cos(pt1[0]) + math.sin(pt2[0]) * math.sin(pt1[0])) + math.sin(pt2[1]) * math.sin(pt1[1]))
  
  
