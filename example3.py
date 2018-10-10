"""
2D half-model with fracture and refinement
"""

from pylagrit import PyLaGriT
import numpy as np
import sys

df = 0.0005     # fault half aperture
lr = 7          # levels of refinement
nx = 4          # number of base mesh blocks in x-dirxn
nz = 20         # number of base mesh blocks in z-dirxn
d_base = df*2**(lr+1)   # calculated dimension of base block
w = d_base*nx   # calculated width of model
d = d_base*nz   # calculated depth of model

lg = PyLaGriT()

# Create discrete fracture mesh
dxyz = np.array([d_base, d_base, 0.])   # spacing b/w pts in x,y,z directions
mins = np.array([0., -d, 0.])
maxs = np.array([w, 0, 0])
mqua = lg.createpts_dxyz(dxyz, mins, maxs, 'quad', hard_bound=('min','max','min'),connect=True)


# Refine elements
for i in range(lr):
    prefine = mqua.pset_geom_xyz(mins-0.1,(0.0001,0.1,0))
    erefine = prefine.eltset()
    erefine.refine()
    prefine.delete()
    erefine.delete()



mtri = mqua.copypts('triplane')
mtri.connect()
# Make sure that no nodes are lost during connect
if 'The mesh is complete but could not include all points.' in lg.before:
    print 'Error: Lost some points during connect, not completing mesh and exiting workflow!'
    print ''
    sys.exit()

mtri.tri_mesh_output_prep()
mtri.reorder_nodes(cycle='xic yic zic')
pfault = mtri.pset_geom_xyz(mins-0.1, (0.0001,0.1,0))
psource = mtri.pset_geom_xyz(mins-0.1,mins+0.0001)
mtri.setatt('imt',1)
pfault.setatt('imt',10)
psource.setatt('imt',20)

mtri.paraview(filename='discrete_fracture.inp')
