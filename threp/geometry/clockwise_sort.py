#! /usr/bin/python
# Filename: clockwise_sort.py

import sys

def clockwise_sort(rect_box):
  '''
  B---C
  |   |
  A---D
  '''
  # check rect_box
  if len(rect_box) != 4:
    print 'invalid input in clockwise_sort function.'
    sys.exit()
  # use default sort of 4 tuples, by cmp the first dim
  rect_box.sort()
  if rect_box[0][1] > rect_box[1][1]:
    rect_box[0], rect_box[1] = rect_box[1], rect_box[0]
  if rect_box[2][1] < rect_box[3][1]:
    rect_box[2], rect_box[3] = rect_box[3], rect_box[2]
  return rect_box

def clockwise_sort_indx(rect_indx, rect_box):
  '''
  B---C
  |   |
  A---D
  '''
  # check rect_box
  if len(rect_box) != 4:
    print 'invalid input in clockwise_sort function.'
    sys.exit()
  # use default sort of 4 tuples, by cmp the first dim
  sort_pair = [(rect_indx[i], rect_box[i]) for i in xrange(len(rect_indx))]
  sort_pair.sort(cmp = lambda x, y:cmp(x[1], y[1]))
  rect_indx = [item[0] for item in sort_pair]
  rect_box = [item[1] for item in sort_pair]
  #rect_box.sort()
  if rect_box[0][1] > rect_box[1][1]:
    rect_indx[0], rect_indx[1] = rect_indx[1], rect_indx[0]
    rect_box[0], rect_box[1] = rect_box[1], rect_box[0]
  if rect_box[2][1] < rect_box[3][1]:
    rect_indx[2], rect_indx[3] = rect_indx[3], rect_indx[2]
    rect_box[2], rect_box[3] = rect_box[3], rect_box[2]
  return rect_indx, rect_box 
