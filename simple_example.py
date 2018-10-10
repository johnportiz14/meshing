"""
pylagrit script for creating a simple cube shaped mesh using
the 'gridder' and connect <pylagrit.PyLaGriT.connect> methods.
"""
# Import PyLaGriT class from pylagrit module
from pylagrit import PyLaGriT

# (at some point, may have to specify pylagritrc file with lagrit_exe path

#---- Create pylagrit object
l = PyLaGriT()

# create xyz arrays for location of points
x = range(1,5)
y = range(1,5)
z = range(1,5)

# create mesh object using xyz arrays
m = l.gridder(x,y,z)

# connect points
m.connect()

#---- visualize connected mesh using ParaView
# (assumes pylagritc is being used)

#  m.paraview()
