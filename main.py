from P3D import *


# example of how to use the class
fname = "./RocFlo-CM.00040000.q"


# create the reader
p3d = PLOT3D_FILE()

# read a file
p3d.read_file(fname)


# grab from grid 0 variable 4 (NOTE: 0 based indexing; grid 1 and variable 5 in FORTRAN)
x = p3d.get_var(0,4)
print "Data from grid 0 and variable 4:\n", x.ravel()

# Set field data to 1.0
x[:,:,:] = 1.0
p3d.set_var(x, 0, 4)

# show update is made
x = p3d.get_var(0,4)
print "\nData from grid 0 and variable 4 (should be 1.0):\n", x.ravel()


# verify file is written correctly
print "\nWrinting PLOT3D data to file 'bob.q'"
p3d.write_file("bob.q")
p3d.read_file("bob.q")

# grab from grid 0 variable 4 (NOTE: 0 based indexing; grid 1 and variable 5 in FORTRAN)
x = p3d.get_var(0,4)
print "\nData from grid 0 and variable 4 (should be 1.0):\n", x.ravel()


