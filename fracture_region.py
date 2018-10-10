"""
Messing around with pylagrit using
the 'gridder' and connect <pylagrit.PyLaGriT.connect> methods.
"""
# Import PyLaGriT class from pylagrit module
from pylagrit import PyLaGriT
import numpy as np

# (at some point, may have to specify pylagritrc file with lagrit_exe path

"""
Define grid dimensions/discretization
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
lg = PyLaGriT()
#---- create mesh object using xyz arrays
m = lg.gridder(x,y,z)
#---- connect points
m.connect()



#---- visualize connected mesh using ParaView
# (assumes pylagritc is being used)
#--THIS NEEDS TO BE HERE     (otherwise mo1.inp file doesn't get created)
m.paraview(filename='fracture_region.inp')



# fault coordinates
cs = [[-0.0005, -10., 0.],
      [-0.0005, 10., 0.],
      [0.0005, 10., 0.],
      [0.0005, 10., -100.],
      [0.0005, -10., -100.],
      [-0.0005, 10., -100.],
      [-0.0005, -10., -100.],
      [-0.0005, -10., -100.]]
cs = np.array(cs)
# create surfaces of fault
ss = []
zipped = zip(cs[:-1],cs[1:])
for p1,p2 in zipped:
    #  p3 = p1.copy() #doesn't work for non-dictionaries (?)
    p3 = list(p1)
    p3[2] = -100.  #????
    ss.append(lg.surface_plane(p1,p2,p3))

# create region by boolean operations of fault surfaces
boolstr = ''
for i,s in enumerate(ss):
    if not i == 0: boolstr += ' and '
    boolstr += 'le '+s.name
r = lg.region_bool(boolstr)
# create pset from region
#  p = motet.pset_region(r)
p = m.pset_region(r)
# Change imt value for pset
p.setatt('imt',21) #makes this zone 21
m.dump_zone_imt('tet_nefault',21)

