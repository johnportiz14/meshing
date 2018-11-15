"""
2D mesh domain of fracture and matrix for
uniform contaminated zone comparison with
3D quarter-sphere cavity.
author: jportiz
7/16/18
"""
from pylagrit import PyLaGriT
import numpy as np
from math import log10


l = PyLaGriT()

# domain lengths in each dimension
xl = 50. #[m] 
yl = 50. #[m]
zl = 100. #[m] depth
df = 0.001 #[m] fracture aperture
largedf = 0.05 #[m] fracture aperture
lr = 3 #levels of mesh refinement
#  d_base = df/2.*2**(lr+1) #calculated dimension of base block
cav_center_depth = 80. #[m] depth of cavity center
radius = 10. #[m] cavity radius

# grid discretization
dx = 1.
dy = 1.
dz = 1.
dxyz = np.array([dx,dy,dz])
#  dxz = np.array([dx,dz])

# (1) ---- Model domain 
x = np.arange(0,xl+dx,dx)
telx = np.concatenate((np.array([0.,df, largedf/2.]), np.logspace(log10(largedf),log10(xl),num=50,endpoint=True)))
#  telx = np.concatenate((np.array([0.,df/2.]), np.logspace(log10(df),log10(xl),num=50,endpoint=True)))

#  y = np.concatenate((np.arange(-yl/2.,0+dy,dy), np.arange(dy,yl/2+dy,dy))) #half-model
#  y = np.arange(0,yl/2+dy,dy) #quarter-model
y = np.arange(0., yl+dy,dy)
z = np.arange(-zl, 0.+dz, dz)
#  z = np.concatenate((np.arange(-zl/2.,0+dz,dz), np.arange(dz,zl/2+dz,dz)))


mins = np.array([min(x), min(y), min(z)])
maxs = np.array([max(x), min(y), max(z)])
#  mins = np.array([min(x), min(z)])
#  maxs = np.array([max(x), max(z)])

#  m = l.gridder(x,y,z,connect=True)
m = l.gridder(telx,y,z,connect=True) #refines toward fracture plane
#  m = l.gridder(telx,z,elem_type='quad',connect=True) #refines toward fracture plane
#  m = l.gridder(telx,z,elem_type='quad') #refines toward fracture plane
#  m.connect()
m.setatt('imt',1) #matrix nodes material set to '1'




#---------------------------------------------------------------------- 
#            FRACTURE
#---------------------------------------------------------------------- 
fmins = np.array([min(x),min(y),min(z)])
#  fmaxs = np.array([df/2.,max(y),max(z)])
fmaxs = np.array([df,max(y),max(z)])
#  fmins = np.array([min(x),min(z)])
#  fmaxs = np.array([df/2.,max(z)])

pfracture = m.pset_geom_xyz(mins=fmins,maxs=fmaxs)
#  pfracture = m.pset_geom(mins=fmins,maxs=fmaxs)
pfracture.setatt('imt', 2)
pfracture.dump('fracture', zonetype='zone')
pfracture.dump('fracture', zonetype='zonn')
#---- manually change zone number in .zonn file
with open('fracture_p1.zonn','r') as file:
    # read list of lines into 'lines'
    lines = file.readlines()
# change the 2nd line of .zonn file, note you have to add newline
lines[1] = '200      fracture\n'
# now write everything back
with open('fracture_p1.zonn','w') as file:
    file.writelines(lines)

#  #---------------------------------------------------------------------- 
#  #            CAVITY
#  #---------------------------------------------------------------------- 
#  #  # Cavity nodes (cuboid formulation) -------------------------- 
#  #  cmins = np.array([0., 0-radius/2., -zl/2.-radius/2.])
#  #  cmaxs = np.array([radius/2., radius/2., -zl/2.+radius/2.])
#  #  pcavity = m.pset_geom_xyz(mins=cmins, maxs=cmaxs, name='cavity')
#  
#  # Cavity nodes (hemisphere formulation) -------------------------
#  cmins = np.array([0., 0-radius/2., -zl/2.-radius/2.])
#  cmaxs = np.array([radius/2., radius/2., -zl/2.+radius/2.])
#  #theta = angle in xy-plane measured from positive x-axis toward positive y-axis
#  #phi = angle measured from positive z-axis to positive y-axis
#  theta1 = 0
#  theta2 = 180
#  phi1 = 0
#  phi2 = 360
#  
#  pcavity = m.pset_geom_rtp(mins=(0.,theta1,phi1), maxs=(radius,theta2,phi2), ctr=(0,0,-cav_center_depth))
#  # change material of cavity nodes
#  pcavity.setatt('imt',3)
#  pcavity.dump('cavity', zonetype='zone')
#  pcavity.dump('cavity', zonetype='zonn')


#---------------------------------------------------------------------- 
#            Other zones
#---------------------------------------------------------------------- 
#---- all top nodes
ptop = m.pset_geom_xyz(mins=(min(x),min(y),-1.e-4),maxs=(max(x),max(y),max(z)))
#  ptop = m.pset_geom_xyz(mins=(min(x),-1.e-4),maxs=(max(x),max(z)))
ptop.dump('top', zonetype='zone')
ptop.dump('top', zonetype='zonn')
#-- manually edit zone number for .zonn file
with open('top_p2.zonn','r') as file:
    lines = file.readlines()
lines[1] = '100      all top nodes\n'
with open('top_p2.zonn','w') as file:
    file.writelines(lines)

#---- top fracture nodes
#  pfractop = m.pset_geom_xyz(mins=(min(x),-1.e-4),maxs=(df/2.,max(z)),name='top')
pfractop = m.pset_geom_xyz(mins=(min(x),min(y),-1.e-4),maxs=(df,max(y),max(z)),name='top')
pfractop.dump('fracture', zonetype='zone')
pfractop.dump('fracture', zonetype='zonn')
#-- manually edit zone number for .zonn file
with open('fracture_top.zonn','r') as file:
    lines = file.readlines()
lines[1] = '101      top fracture nodes\n'
with open('fracture_top.zonn','w') as file:
    file.writelines(lines)

#  m.dump_fehm('fm_2D')
m.dump_fehm('mesh_uniform_contam_zone')
m.paraview(filename='mesh_uniform_contam_zone.inp')




#  
#  #  # change material of cavity nodes
#  #  pcavity.setatt('imt',2)
#  #  
#  #  
#  #  m.paraview('fmc_mesh.inp')
#  #  
