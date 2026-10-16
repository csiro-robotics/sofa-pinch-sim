# sofa-fin
## This project simulates a pair of fin-ray fingers performing pinch grasps of 36 objects. 

To run the simulation, you need to install SOFA under Ubuntu environment (20.04). 

Add the following plugins into SOFA/lib/plugin_list.conf (not the default version):
SofaPython3 1.0
STLIB 3.0
ArticulatedSystemPlugin 23.06.00

Important: Set environmental variables in bashrc. For example:
- PYTHON_ROOT=/usr/bin/python3.8
- SOFA_ROOT=/home/lio011/SOFA
- SOFAPYTHON3_ROOT=/home/lio011/SOFA/plugins/SofaPython3
- PYTHONPATH=/home/lio011/SOFA/plugins/SofaPython3/lib/python3/site-packages:/home/lio011/SOFA/plugins/SoftRobots/lib/python3/site-packages:/home/lio011/SOFA/plugins/STLIB/lib/python3/site-packages:/home/lio011/SOFA/plugins/SofaPython3/lib/python3/site-packages

Clone pinch_STEPupdate branch. This branch has the latest .STEP files for objects, and are configured to be in the right order (object_0 to object_35) and orientation as the physical setup in gantry.

Run python3.8 final.py


### Helpful tips:
In final.py, uncomment out this line to view GUI of the pinch grasps:
cmd = f'{bash} -a grasping_3.py --argv {mesh_name} --argv {object_name} --argv {object_depth} --argv {basic_name}'

----------------------------------------------------------------------------------------------------------------------
## Fixes
### 11/10/2023
- final.py: 
Adjusted finger generation lower and upper bounds to ensure that there is a minimum of 2mm thickness for the fins and bases for printing. 

Created new variable called 'batch_name' to create labels on the fingers. This variable is then passed onto fin_design function in finray_design_auto.py. Please update this string variable each time a new batch is created.

- finray_design_auto.py
Fixed rib overextrusion problem. 
Fixed orientation problem for exported whole finger .STEP files, in which the fin and bases were rotated by 90 degrees.

### 04/10/2023 and earlier revisions
- Folder: data/objectstep
Updated latest object .STEP files with naming convention the same as gantry (object_0 to object_35). Object .STL files are regenerated using auto_mesh_stl.py and exported to data/object.

- grasping_3.py 
Rotated objects by 90 degrees to ensure pinch direction is the same as gantry.