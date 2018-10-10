"""
https://lanl.github.io/LaGriT/pages/docs/tutorial.html
This tutorial explains how to generate a grid in a
unit cube containing two materials separated by a
plane. (translated from LaGriT to PyLaGriT)
"""

from pylagrit import PyLaGriT
import numpy as np

"""
(1) Define mesh objects
---------------------------------------------------
- create a 3D tetrahedral mesh object and name it 3dmesh
"""
lg = PyLaGriT()
m = lg.create(name='3Dmesh')

"""
(2) Define an enclosing volume
---------------------------------------------------
- Define an enclosing volume using the surface command
- Since we are defining an exterior boundary, the boundary type is reflect.
"""
#  # not really sure how to do this in pylagrit...
#  mini = 0.0
#  maxi = 1.0
#  x = np.array([mini,maxi])
#  y = x
#  z = y
#  
#  cube = lg.gridder(x,y,z)

#----
cube = lg.surface_box([0.,0.,0.],[1.,1.,1.], name='cube', ibtype='reflect')


"""
(3) Define interior interfaces
---------------------------------------------------
- Interfaces are defined with the surface command.
- In this case the boundary type is intrface
- divide the unit cube defined above in half vertically
"""

cutplane = lg.surface_plane([0.,0.,0.5],[1.,0.,0.5],[1.,1.,0.5], name='cutplane', ibtype='intrface')

"""
(4) Divide the enclosing volume into regions
---------------------------------------------------
-  define the two regions created by the plane bisecting the unit cube
- The region command is used to divide the enclosing volume into regions.
- The directional operators lt, le, gt, ** ** and ge are applied to previously defined surfaces according to the rules.
"""

# 'top' region: includes top half of cube and non of the interface (cutplane)
#--- LaGriT command: 'region/top le cube and gt cutplane'
# PyLaGriT: create region by boolean operations
top_boolstr = 'le cube and gt cutplane'
top = lg.region_bool(top_boolstr, name='top')
#  top = m.region_bool(top_boolstr, name='top')

# 'bottom' region: includes bottom half of cube and cutplane
#--- LaGriT command: 'region/bottom le cube and lt cutplane'
# PyLaGriT: create region by boolean operations
bot_boolstr = 'le cube and le cutplane'
bot = lg.region_bool(bot_boolstr, name='bottom')
#  bot = m.region_bool(bot_boolstr, name='bottom')

"""
(5) Assign material types to the regions
---------------------------------------------------
- Assign materials to regions using the mregion command
- Assign two materials, mattop and matbot, to the regions top and bottom
"""
#--- LaGriT commands:
# mregion/ mattop/ le cube and gt cutplane 
# mregion/ matbot/ le cube and lt cutplane

tm_boolstr = 'le cube and gt cutplane'
bm_boolstr = 'le cube and lt cutplane'

# maybe it's   m.pset_attribute()    ???
# ..........
# maybe can just define them as regions, same as before...
#  # mregion has similar syntax to region command
mat_top = lg.region_bool(tm_boolstr, name='mattop')
mat_bot = lg.region_bool(bm_boolstr, name='matbot')
#  mat_top = m.region_bool(tm_boolstr, name='mattop')
#  mat_bot = m.region_bool(bm_boolstr, name='matbot')


"""
(6) Distribute points within the volume
---------------------------------------------------
- Many methods: for simple geometries we use the createpts (and regnpts) command
- points are distributed within regions by constructing rays through regions and distributing points along these rays.
- createpts command creates the points
- regnpts specifies the plane, region, and number of points distributed along the rays.
"""

# - create 25 points (5x5x1) in a plane above the unit cube
# - place points on the boundaries in the x and y directions (1,1,0)
#-----lagrit: createpts /xyz/5,5,1/0.,0.,1.1/1.,1.,1.1/1,1,0
#  abovepts = lg.createpts(crd='xyz', npts=(5,5,1), mins=(0.,0.,1.1), maxs=(1.,1.,1.1), rz_switch=(1,1,0)) # not sure if this is correct
abovepts = m.createpts(crd='xyz', npts=(5,5,1), mins=(0.,0.,1.1), maxs=(1.,1.,1.1), rz_switch=(1,1,0)) # not sure if this is correct
# give the points defined by the createpts command the name, rayend
#-----lagrit: pset/rayend/seq/1,0,0/
m.pset_geom(name='rayend',stride=(1,0,0), mins=(0,0,1.1), maxs=(1.,1.,1.1))

# -  create rays between points in rayend and the plane below the cube
# -  distribute 3 points along these rays in the region top
# -  add one point at the upper external boundary for each ray
# -  will get 4 points total along each ray in region top
# -  "pset,get,rayend" refers to all the points named rayend
# -  the three points: (0.,0.,-.1), (0.,1.,-.1), (1.,1.,-.1)
# -  define a plane whose normal points toward the rayend points
#-------lagrit: regnpts/top/3/pset,get,rayend/xyz/0.,0.,-.1/0.,1.,-.1/1.,1.,-.1/0,0

######  STUCK HERE... NOT SURE HOW TO ACHIEVE WHAT'S DONE IN: https://lanl.github.io/LaGriT/pages/docs/distributep.html ##################

m.pset_region(region='top', stride=(0,0,3)) #stride may be wrong here


