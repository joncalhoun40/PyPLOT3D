from P3D import *


# example of how to use the class
fname = "./RocFlo-CM.00040000.q"


# create the reader
p3d = PLOT3D_FILE()

# read a file
p3d.read_file(fname)

# grab from grid 0 variable 4 (NOTE: 0 based indexing; grid 1 and variable 5 in FORTRAN)
print (p3d.get_var(0,4).ravel()) # .ravel() converts to 1D array
x = p3d.get_var(0,4).ravel() # .ravel() converts to 1D array
import matplotlib.pyplot as plt
plt.hist(x, range=[-1e-7, 1e-7], bins = 100)
plt.ylim((0, x.shape[0]+100))
#plt.savefig("./fhisto." + "." + str(i) + ".png")
plt.show()
