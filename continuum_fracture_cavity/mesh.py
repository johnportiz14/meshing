"""
3D Quarter-model mesh domain of fracture and cavity (no matrix).
author: jportiz
11/15/18
"""
from pylagrit import PyLaGriT
import numpy as np
from math import log10


l = PyLaGriT()

# domain lengths in each dimension
xl = 50. #[m] 
yl = 50. #[m]
zl = 100. #[m] depth
df = 0.05
largedf = 0.05 #[m] fracture aperture
lr = 3 #levels of mesh refinement
#  d_base = df/2.*2**(lr+1) #calculated dimension of base block
cav_center_depth = 70. #[m] depth of cavity center
radius = 20. #[m] cavity radius

# grid discretization
dx = 1.
dy = 1.
dz = 1.
dxyz = np.array([dx,dy,dz])

# (1) ---- Model domain 
x = np.arange(0,xl+dx,dx)
#  telx = np.concatenate((np.array([0.,df, largedf/2.]), np.logspace(log10(largedf),log10(xl),num=50,endpoint=True)))
telx = np.concatenate((np.array([0.,df]), df+np.logspace(log10(df),log10(xl),num=25,endpoint=True)))
np.diff([0.0, df)]+np.logspace(-2,log10(xl),50)



#  y = np.concatenate((np.arange(-yl/2.,0+dy,dy), np.arange(dy,yl/2+dy,dy))) #half-model
#  y = np.arange(0,yl/2+dy,dy) #quarter-model
y = np.arange(0,yl+dy,dy) #quarter-model
z = np.arange(-zl, 0.+dz, dz)
#  z = np.concatenate((np.arange(-zl/2.,0+dz,dz), np.arange(dz,zl/2+dz,dz)))


mins = np.array([min(x), min(y), min(z)])
maxs = np.array([max(x), max(y), max(z)])


#  m = l.gridder(telx,y,z,connect=True) #refines toward fracture plane
m = l.gridder(telx,y,z,connect=False) #refines toward fracture plane            #NEW

m.setatt('imt',2) #matrix nodes material set to '2'

l.sendline('filter / 1 0 0 /; rmpoint compress')
l.sendline('cmo printatt mo1 -all- minmax')



m.connect()

m.setatt('imt',2) #matrix nodes material set to '2'




#---------------------------------------------------------------------- 
#            FRACTURE PLANE
#---------------------------------------------------------------------- 
fmins = np.array([min(x),min(y),min(z)])
#  fmaxs = np.array([df/2.,max(y),max(z)])
fmaxs = np.array([df-1.e-5,max(y),max(z)])

pfracture = m.pset_geom_xyz(mins=fmins,maxs=fmaxs)
pfracture.setatt('imt', 1)
#  pfracture.dump('fracture', zonetype='zone')
#  pfracture.dump('fracture', zonetype='zonn')



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
#  pcavity.dump('cavity', zonetype='zone')
#  pcavity.dump('cavity', zonetype='zonn')







# dump initial viz mesh before removing matrix
#  m.connect() # NEW (11/19/18)
m.dump('initialmesh.inp')
m.dump_lg('initialmesh')

#--------------------------------
#       Remove matrix nodes
#--------------------------------
# grab all points with imt=2 (matrix nodes)
#  m.rmpoint_pset(pset=pmatrix,compress=True,itype='exclusive')
#======== This part messes up the node connections around cavity =======
#  pmatrix = m.pset_attribute(attribute='imt',value=2)
#  m.filter()
#  m.tri_mesh_output_prep()
#  m.rmpoint_pset(pset=pmatrix,compress=True,resetpts_itp=False)
#  m.rmpoint_pset(pset=pmatrix,compress=False,resetpts_itp=False)
#  m.filter()
#  m.tri_mesh_output_prep()
#  m.rmpoint_pset(pset=pmatrix,compress=True)
#  m.rmpoint_pset(pset=pmatrix,compress=True)
#  m.rmpoint_compress(filter_bool=True)
#======================================================================= 

#  m.tri_mesh_output_prep()
#  m.connect() # NEW (11/19/18)
#  m.tri_mesh_output_prep()
#  m.filter()
#  m.tri_mesh_output_prep()
m.dump('step2.inp')

#  #  #---re-classify the fracture and cavity zones
#  #FRACTURE
#  #grab entire fracture plane
#  fmaxs = np.array([df,max(y),max(z)])
#  pfracture = m.pset_geom_xyz(mins=fmins,maxs=fmaxs)
#  pfracture.setatt('imt', 1)
#  pfracture.dump('fracture', zonetype='zonn')
#  #CAVITY
#  #make everything not fracture set to imt=3
#  pcavity1 = m.pset_attribute(attribute='imt',value=1,comparison='ne')
#  pcavity1.setatt('imt',3)
#  #now grab cavity nodes that are in the fracture plane
#  pcavity2 = m.pset_geom_rtp(mins=(0.,theta1,phi1), maxs=(radius+9.e-1,theta2,phi2), ctr=(0,0,-cav_center_depth))
#  pcavity2.setatt('imt',3)
#  #combine pcavity1 and pcavity2 into single pset
#  pcavity = m.pset_attribute(attribute='imt',value=3)
#  pcavity.dump('cavity', zonetype='zonn')
#  #infile / initialmesh.lg
#  
#  m.tri_mesh_output_prep()
#  
#  #----------------------------------------------
#  #            Other zones
#  #----------------------------------------------
#  # all top nodes
#  ptop = m.pset_geom_xyz(mins=(min(x),min(y),-1.e-4),maxs=(max(x),max(y),max(z)))
#  ptop.dump('top', zonetype='zone')
#  ptop.dump('top', zonetype='zonn')
#  #  m.smooth()
#  #  m.recon(0)
#  #  m.smooth()
#  #  m.recon(0)
#  #  m.smooth()
#  #  m.recon(0)
#  
#  m.tri_mesh_output_prep()
#  #  m.connect()     #NEW (11/19/18)

m.dump('continuum_fracture_cavity.inp')
m.dump_fehm('continuum_fracture_cavity')

#  
#  # dump lagrit binary file that can be read into a .lgi input file for further tweaking
#  m.dump_lg('initialmesh.lg')
#  # dump viz file
#  
