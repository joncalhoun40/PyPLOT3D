import numpy as np
import fortranfile as fofi

class PLOT3D_FILE:
    """
    Python reader for NASA Plot3D file written by a Fortran application.
    Note: Only reads data. Write support in latter version.
    """

    def __init__(self):
        self.ngrids = 1
        self.grids = None
        self.dims = None
        self.ndim = 3   # Assume 3D data
        self.nvar = 5   # Assume 3D data
        
        self.mach = 0
        self.alpha = 0
        self.reynolds = 0
        self.time = 0

    def read_file(self, filename, read2D = False, endian='>', header_prec='i', data_prec='d'):
        """
        Reads a PLOT3D file 'filename' from disk and stores its contents in
        memory
        
        Parameters
        ----------
        filename : string
            Name of the file to read
        read2D  : boolean
            [optional] Is the file in a 2d data format?
        endian : character
            [optional]endianness of the file. '>' for little-endian; '<' for big-endian
        header_prec : character
            [optional] precision of integer data types. 'i' for 4-byte; 'l' for 8-byte
        data_prec : character
            [optional] precision of floating-point data types. 'f' for 4-byte; 'd' for 8-byte
        
        """
        
        f = fofi.FortranFile(filename,endian,header_prec)
        self.dim = 3
        self.nvar = 5
        if read2D == True:
            self.ndim = 2
            self.nvar = 4
        
        # read the file header
        self.ngrids = f.readInts()[0]
        self.dims = np.zeros( (self.ngrids, self.ndim), dtype=np.int32) #3D data
        grid_dims = f.readInts()

        #read the grid dims 
        for i in xrange(self.ngrids):
            self.dims[i,:] = grid_dims[self.ndim*i : self.ndim*(i+1)]

        #clean up from previous file
        if self.grids != None:
            for i in xrange(self.ngrids):
                #if self.grids[i] != None:
                del self.grids[0]
        del self.grids
        self.grids = []

        # read the grid data
        for i in xrange(self.ngrids):
            #read scalars
            self.mach, self.alpha, self.renolds, self.time  = np.array( f.readReals(data_prec) )

            data = np.array( f.readReals(data_prec) )
            if self.ndim == 3:
                shape = (self.dims[i][0], self.dims[i][1], self.dims[i][2], self.nvar)
            else:
                shape = (self.dims[i][0], self.dims[i][1], self.nvar)
            data = np.reshape(data, shape, order='F')
            self.grids.append( data )



    def get_var(self, grid, i):
        """
        Returns an array for a variable 'i' on grid 'grid'

        Parameters
        ----------
        grid : integer
            grid number to extract data from
        i : integer
            varable on the 'grid' you want data from

        Raises
        ------
        ValueError
            when grid or varaiable does not exist
        """
        if grid >= 0 and grid < self.ngrids and i >= 0 and i < self.nvar:
            if self.ndim == 3:
                return self.grids[grid][:,:,:,i]
            else:
                return self.grids[grid][:,:,i]
        else:
            raise ValueError('could not find variable %d on grid %d' %(i, grid))
            return None
"""    
#========================================================================
#========================================================================
#========================================================================


# example of how to use the class
fname = "./RocFlo-CM.00010000.q"
fname2 = "./RocFlo-CM.00035000.q"


# create the reader
p3d = PLOT3D_FILE()

# read a file
p3d.read_file(fname)

# grab from grid 0 variable 4 (NOTE: 0 based indexing; grid 1 and variable 5 in FORTRAN)
print p3d.get_var(0,0).ravel() # .ravel() converts to 1D array

# read a file
p3d.read_file(fname2)

# grab from grid 0 variable 4 (NOTE: 0 based indexing; grid 1 and variable 5 in FORTRAN)
print p3d.get_var(0,0).ravel() # .ravel() converts to 1D array
"""
