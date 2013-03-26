#! /usr/bin/python
# Filename: show.py

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import sys
import Tkinter as Tk
import ttk 
import Tix
import threp_import
import bilinear

def remap_entry(src_file, dst_file, alg_name, real_data_file, offline_flag, pole_flag):
  if offline_flag:
    test_obj = alg_name(src_file, dst_file, False, real_data_file, pole_flag)
  else:
    test_obj = alg_name(src_file, dst_file, True, real_data_file)
  test_obj.interp()
  if offline_flag:
    test_obj.gen_remap_matrix_file()
  else:
    remap_result = test_obj.remap()
    print remap_result

def demo(value):
  print 'hello'
  print value

def validate_entry():
  pass

def offline_menu():
  grid_lst = ['Gamil_128x60_Gaussian_Grid', 'Gamil_360x180_Gaussian_Grid', 'T42_Gaussian_Grid', 'T62_Gaussian_Grid', 'T85_Gaussian_Grid', 'licom_eq1x1', 'LICOM_P5', 'POP43', 'licom_gr1x1'] 
  board = Tk.Tk()
  board.title('OFFLINE REMAPPING BOARD')
  variable_src_grid_file = Tk.StringVar(board, 'T42_Gaussian_Grid')
  #variable_src_grid_file = Tk.StringVar(board, '')
  Tk.Label(board, text = 'Source Grid: ').pack(side = 'left')
  ttk.Combobox(board, textvariable = variable_src_grid_file, values = grid_lst).pack(side = 'left')
  variable_dst_grid_file = Tk.StringVar(board, 'POP43')
  #variable_dst_grid_file = Tk.StringVar(board, '')
  Tk.Label(board, text = ' Destination Grid: ').pack(side = 'left')
  ttk.Combobox(board, textvariable = variable_dst_grid_file, values = grid_lst).pack(side = 'left')
  variable_alg_name = Tk.StringVar(board, 'Bilinear')
  Tk.Label(board, text = ' Algorithm Name: ').pack(side = 'left')
  ttk.Combobox(board, textvariable = variable_alg_name, values=['Bilinear', 'Idw', 'Conservation', 'Spline', 'Bicubic']).pack(side = 'left')
  variable_pole_option = Tk.StringVar(board, 'None')
  Tk.Label(board, text = ' Pole Option: ').pack(side = 'left')
  ttk.Combobox(board, textvariable = variable_pole_option, values=['none', 'all']).pack(side = 'left')
  #remap_button = Tk.Button(board, text = 'Remap', command = lambda: demo(val))
  remap_button = Tk.Button(board, text = 'Remap', command = lambda: remap_entry('../../grid/T42_Gaussian_POP43/POP43.nc', '../../grid/T42_Gaussian_POP43/T42_Gaussian.nc', bilinear.Bilinear, 'null', True, False))
  remap_button.pack(side = 'left')
  board.mainloop() 

def online_menu():
  pass

def validate_menu():
  board = Tk.Tk()
  board.title('Validate Menu')
  variable_analysis = Tk.StringVar(board, 'function1')
  Tk.Label(board, text = 'Analysis Function: ').pack(side = 'top', anchor = 'center')
  ttk.Combobox(board, textvariable = variable_analysis, values = ['function1', 'function2', 'function3']).pack(side = 'top', anchor = 'center')
  variable_real = Tk.StringVar(board, '')
  Tk.Label(board, text = 'Real Data: ').pack(side = 'top', anchor = 'center')
  ttk.Combobox(board, textvariable = variable_real, values = ['T42_Gaussian']).pack(side = 'top', anchor = 'center')
  validate_button= Tk.Button(board, text = 'Validate', command = validate_entry)
  validate_button.pack(side = 'bottom', anchor = 'center')
  board.mainloop() 

if __name__ == '__main__':
  main = Tk.Tk()
  main.title('Main Menu')
  Tk.Label(main, text = 'THREP(TsingHua REgridding Platform) v1.0').pack(side = 'bottom', anchor = 'center')
  win = Tk.Frame(main, height = 30, width = 50)
  win.pack(side = 'top', anchor = 'center')
  offline_button = Tk.Button(main, text = 'OFFLINE', command = offline_menu, height = 3, width = 15)
  offline_button.pack(side = 'top', anchor = 'center')
  online_button = Tk.Button(main, text = 'ONLINE', command = online_menu, height = 3, width = 15)
  online_button.pack(side = 'top', anchor = 'center')
  validation_button = Tk.Button(main, text = 'VALIDATION', command = validate_menu, height = 3, width = 15)
  validation_button.pack(side = 'top')
  main.mainloop() 

