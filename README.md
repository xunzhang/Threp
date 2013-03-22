Threp Overview
==============

Interpolation is a bridge links the discrete space to the continuous space, in other words, real solutions to theories, so it's great!

Interpolation in Coupled Earth System Model is something called 'Remap' or 'Regridding'. It's a special application of interpolation. 

Also, it is a little different from traditional interpolation in Computer Graphics. We must seperate the interpolation here into two step:i). Generate weights, ii). Calculate values, according to the specific application scene. What's more, interpolation here happens on surface of the earth, so we must take 'Polar Problem' and 'Periodic Boundary Problem' into account. More importantly, we must 'keep conservative' during flux remapping process..

Embrace Threp!


Installation
------------
I. Install NumPy Python Library. NumPy is the fundamental package for scientific computing with Python. See more infomation at http://www.numpy.org.
II. Install MPI4Py Python Library. MPI4Py is a Python version of MPI. See more infomation at http://mpi4py.scipy.org. 
III. Install Scientific Python Library to support NetCDF(a kind of binary file) file format in Threp, see more infomation at http://gfesuite.noaa.gov/developer/netCDFPythonInterface.html.
IV. Define environment variable 'THREP_DIR' in $THREP_DIR/config/threp_dir.py, and then type

``` bash
<<<<<<< HEAD:README.md
$ python install.py
=======
 $python install.py
>>>>>>> fb5f7f3b514860a976b6d79a6f706d57f0ada762:README
```

V. Now you are successfully installed Threp, have fun.


Tests
-----
Example for generating a remapping weight file:

``` bash
<<<<<<< HEAD:README.md
$ cd $THREP_DIR/../bin/wgen/
$ python remap_entry.py	# serial
$ mpirun -n $num python remap_entry.py	# parallel
=======
 $cd $THREP_DIR/../bin/wgen/
 $python remap_entry.py	# serial
 $mpirun -n $num python remap_entry.py	# parallel
>>>>>>> fb5f7f3b514860a976b6d79a6f706d57f0ada762:README
```  

Here, you can modify remap_entry.py file(line 42) to reset your input. 
Python2.7 or earlier tested.

Example for developing a new remapping algorithm:
  Create a algname.py at $THREP_DIR/interp/algs.
  Write a class which inherit the Interp superclass, that means you can use lots of functions in class Interp.
  Rewrite interp method in your newalg class, just a long loop(100~200 LOC)
