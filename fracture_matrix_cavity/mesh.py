"""
3D Half-model mesh domain of fracture, matrix,
and simplified explosion cavity (cube).
author: jportiz
6/29/18
"""
from pylagrit import PyLaGriT
import numpy as np
from math import log10


l = PyLaGriT()

# domain lengths in each dimension
xl = 50. #[m] 
yl = 50. #[m]
zl = 100. #[m] depth
df = 0.01 #[m] fracture aperture
lr = 3 #levels of mesh refinement
d_base = df/2.*2**(lr+1) #calculated dimension of base block
cav_center_depth = 70. #[m] depth of cavity center
radius = 20. #[m] cavity radius

# grid discretization
dx = 1.
dy = 1.
dz = 1.
dxyz = np.array([dx,dy,dz])

# (1) ---- Model domain 
x = np.arange(0,xl+dx,dx)
telx = np.concatenate((np.array([0.,df/2.]), np.logspace(log10(df),log10(xl),num=50,endpoint=True)))

y = np.concatenate((np.arange(-yl/2.,0+dy,dy), np.arange(dy,yl/2+dy,dy)))
z = np.arange(-zl, 0.+dz, dz)
#  z = np.concatenate((np.arange(-zl/2.,0+dz,dz), np.arange(dz,zl/2+dz,dz)))


mins = np.array([min(x), min(y), min(z)])
maxs = np.array([max(x), max(y), max(z)])

#  m = l.gridder(x,y,z,connect=True)
m = l.gridder(telx,y,z,connect=True) #refines toward fracture plane
m.setatt('imt',1) #matrix nodes material set to '1'




#---------------------------------------------------------------------- 
#            FRACTURE PLANE
#---------------------------------------------------------------------- 
fmins = np.array([min(x),min(y),min(z)])
fmaxs = np.array([df/2.,max(y),max(z)])

pfracture = m.pset_geom_xyz(mins=fmins,maxs=fmaxs)
pfracture.setatt('imt', 2)
pfracture.dump('fracture', zonetype='zone')
pfracture.dump('fracture', zonetype='zonn')



#---------------------------------------------------------------------- 
#            CAVITY
#---------------------------------------------------------------------- 
#  # Cavity nodes (cuboid formulation) -------------------------- 
#  cmins = np.array([0., 0-radius/2., -zl/2.-radius/2.])
#  cmaxs = np.array([radius/2., radius/2., -zl/2.+radius/2.])
#  pcavity = m.pset_geom_xyz(mins=cmins, maxs=cmaxs, name='cavity')

# Cavity nodes (hemisphere formulation) -------------------------
cmins = np.array([0., 0-radius/2., -zl/2.-radius/2.])
cmaxs = np.array([radius/2., radius/2., -zl/2.+radius/2.])
#theta = angle in xy-plane measured from positive x-axis toward positive y-axis
#phi = angle measured from positive z-axis to positive y-axis
theta1 = 0
theta2 = 180
phi1 = 0
phi2 = 360

pcavity = m.pset_geom_rtp(mins=(0.,theta1,phi1), maxs=(radius,theta2,phi2), ctr=(0,0,-cav_center_depth))
# change material of cavity nodes
pcavity.setatt('imt',3)
pcavity.dump('cavity', zonetype='zone')
pcavity.dump('cavity', zonetype='zonn')


#---------------------------------------------------------------------- 
#            Other zones
#---------------------------------------------------------------------- 
# all top nodes
ptop = m.pset_geom_xyz(mins=(min(x),min(y),-1.e-4),maxs=(max(x),max(y),max(z)))
ptop.dump('top', zonetype='zone')
ptop.dump('top', zonetype='zonn')
# top fracture nodes
pfractop = m.pset_geom_xyz(mins=(min(x),min(y),-1.e-4),maxs=(df/2.,max(y),max(z)),name='top')
pfractop.dump('fracture', zonetype='zone')
pfractop.dump('fracture', zonetype='zonn')




#  m.paraview(filename='fmc_mesh_hemisphere.inp')
m.dump_fehm('fmc_plane_mesh_hemisphere')
m.paraview(filename='fmc_plane_mesh_hemisphere.inp')




#  
#  #  # change material of cavity nodes
#  #  pcavity.setatt('imt',2)
#  #  
#  #  
#  #  m.paraview('fmc_mesh.inp')
#  #  
