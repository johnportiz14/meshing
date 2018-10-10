--------------------------------------------------------
These files are from a workflow given to me by Nataliia. 
--------------------------------------------------------

I am sending you the files and below is the workflow to run a case shown in attached screen shot: triangular mesh on plane crossing 3D volume tets in a cylinder.

1.  Run LAGRIT with  cylinder_plane.lgi inputs. The following output files are necessary:
           plane.stor // stor file of the plane
           cylinder.stor // stor file of the cylinder
           cyl_plane.fehmn // combined mesh connectivity file 
           cyl_plane.inp // combined avs file
           common_pts1.table & common_pts2.table // tables needed for MD nodes list

2.   Run ./createmdnodes  This executable (I'm sending the source C file as well) generates MDnodes list that will be used by FEHM and outputs updated cyl_plane.fehmn, where the connectivity list is fixed with combination of try and tet elements.


3. The next step is to get the volume (or aperture) of the plane. The code (stor2d3d_tf ) will ask to enter the thickness of the plane and will fix volume and area in the store   file of the plane according to the entered thickness.
          cp plane.stor tri_fracture.stor
          ./stor2d3d_tf
           cp tri_fracture.stor plane.stor 

4. The last step is to combine stor files into one, cyl_plane.stor
            ./addmergedstor
     
As a result you will have three files that are necessary to run FEHM: MDnodes; cyl_plane.fehmn; cyl_plane.stor.  
I'm sending you all the source files with executables, if something doesn't work or you need any changes - feel free to change code and upgrade it as you wish. This code is written more than 5 years ago, so...
