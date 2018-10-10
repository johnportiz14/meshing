"""
Larger octree full mesh for transient DFN comparisons
"""
# Import PyLaGriT class from pylagrit module
from pylagrit import PyLaGriT
import numpy as np

# (at some point, may have to specify pylagritrc file with lagrit_exe path

"""
Grid dimensions/discretization
"""
#---- Dimensions
dm = 10.        #[m] half-block width
df = 0.001      #[m] fracture aperture
L = 100.        #[m] total domain depth
#---- Discretization
dx = 1.         #[m] matrix horz. discretization
dy = dx         # same as dx
dz = 1.         #[m] 

"""
Create xyz arrays for location of points
"""
#-----
#  X
#-----
# blocks on either side of the fracture
l_block = np.linspace(-dm, -df/2, 10)   # left block
r_block = -1 * l_block[::-1]            # right block 
# assemble
x = np.concatenate((l_block, r_block), axis=0)
#-----
#  Y
#-----
y = x       #for now, same as x
#-----
#  Z
#-----
z = np.linspace(-L, 0., int(L)+1)


"""
Build mesh
"""
#---- Create pylagrit object
l = PyLaGriT()
#---- create mesh object using xyz arrays in gridder
m = l.gridder(x,y,z)
#---- connect points
m.connect()

#---- visualize connected mesh using ParaView
# (assumes pylagritc is being used)
#--THIS NEEDS TO BE HERE     (otherwise mo1.inp file doesn't get created)
m.paraview() # will throw an error on server, can still view mo1.inp on locally mounted paraview


