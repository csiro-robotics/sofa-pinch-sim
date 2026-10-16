# ------------------------------------------------------------------------------
#  Gmsh Python 
#  STEP import and manipulation, geometry partitioning
# ------------------------------------------------------------------------------

# The OpenCASCADE CAD kernel allows to import STEP files and to modify them. 

import gmsh
import math
import sys

# path_finger
# finger_mesh=True produces a .msh file
# finger_mesh=False produces a .stl file

def mesh(path_finger, mesh_sizes, design_name, surf=False, finger_mesh=True):
    gmsh.initialize()
    gmsh.model.add("finger")

    # Load a STEP file (using `importShapes' instead of `merge' allows to directly
    # retrieve the tags of the highest dimensional imported entities):

    v = gmsh.model.occ.import_shapes(path_finger)

    # If we had specified
    # gmsh.option.setString('Geometry.OCCTargetUnit', 'M')
    # before merging the STEP file, OpenCASCADE would have converted the units to
    # meters (instead of the default, which is millimeters).

    # Get the bounding box of the volume:
    xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.occ.getBoundingBox(
        v[0][0], v[0][1])

    # We want to slice the model into N slices, and either keep the volume slices
    # or just the surfaces obtained by the cutting:

    N = 2  # Number of slices
    dir = 'Z' # Direction: 'X', 'Y' or 'Z'
    # surf = False  # Keep only surfs

    dx = (xmax - xmin)
    dy = (ymax - ymin)
    dz = (zmax - zmin)
    L = dz if (dir == 'X') else dx
    H = dz if (dir == 'Y') else dy

    # Create the first cutting plane:
    s = []
    s.append((2, gmsh.model.occ.addRectangle(xmin, ymin, zmin, L, H)))
    if dir == 'X':
        gmsh.model.occ.rotate([s[0]], xmin, ymin, zmin, 0, 1, 0, -math.pi/2)
    elif dir == 'Y':
        gmsh.model.occ.rotate([s[0]], xmin, ymin, zmin, 1, 0, 0, math.pi/2)
    tx = dx / N if (dir == 'X') else 0
    ty = dy / N if (dir == 'Y') else 0
    tz = dz / N if (dir == 'Z') else 0
    gmsh.model.occ.translate([s[0]], tx, ty, tz)

    # Create the other cutting planes:
    for i in range(1, N-1):
        s.extend(gmsh.model.occ.copy([s[0]]))
        gmsh.model.occ.translate([s[-1]], i * tx, i * ty, i * tz)

    # Fragment (i.e. intersect) the volume with all the cutting planes:
    gmsh.model.occ.fragment(v, s)

    # Now remove all the surfaces (and their bounding entities) that are not on the
    # boundary of a volume, i.e. the parts of the cutting planes that "stick out" of
    # the volume:
    gmsh.model.occ.remove(gmsh.model.occ.getEntities(2), True)

    gmsh.model.occ.synchronize()

    if surf:
        # If we want to only keep the surfaces, retrieve the surfaces in bounding
        # boxes around the cutting planes...
        eps = 1e-3
        s = []
        for i in range(1, N):
            xx = xmin if (dir == 'X') else xmax
            yy = ymin if (dir == 'Y') else ymax
            zz = zmin if (dir == 'Z') else zmax
            s.extend(gmsh.model.getEntitiesInBoundingBox(
                xmin - eps + i * tx, ymin - eps + i * ty, zmin - eps + i * tz,
                xx + eps + i * tx, yy + eps + i * ty, zz + eps + i * tz, 2))
        # ...and remove all the other entities (here directly in the model, as we
        # won't modify any OpenCASCADE entities later on):
        dels = gmsh.model.getEntities(2)
        for e in s:
            dels.remove(e)
        gmsh.model.removeEntities(gmsh.model.getEntities(3))
        gmsh.model.removeEntities(dels)
        gmsh.model.removeEntities(gmsh.model.getEntities(1))
        gmsh.model.removeEntities(gmsh.model.getEntities(0))

    # Finally, let's specify a global mesh size and mesh the partitioned model:
    # minMeshSize = round(float(sys.argv[2]), 2)
    # maxMeshSize = round(float(sys.argv[3]), 2)
    # curvatureSetting = round(float(sys.argv[4]), 2)

    # mesh_sizes = [1, 2, 3, 2]

    # Manual Override
    sizefactor = mesh_sizes[0]
    minMeshSize = mesh_sizes[1]
    maxMeshSize = mesh_sizes[2]
    curvatureSetting = mesh_sizes[3]

    

    gmsh.option.setNumber("Mesh.MeshSizeFactor", sizefactor)
    gmsh.option.setNumber("Mesh.MeshSizeMin", minMeshSize)
    gmsh.option.setNumber("Mesh.MeshSizeMax", maxMeshSize)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", curvatureSetting)
    gmsh.model.mesh.generate(3)

    a = str(design_name)

    
    if finger_mesh:
        gmsh.write(f"data/mesh/fem-{a}-{minMeshSize}-{maxMeshSize}-{curvatureSetting}.msh")

        mesh_name = f'/mesh/fem-{a}-{minMeshSize}-{maxMeshSize}-{curvatureSetting}.msh'

    else:
        gmsh.write(f"data/mesh/basic-{a}-{minMeshSize}-{maxMeshSize}-{curvatureSetting}.stl")

        mesh_name = f'/mesh/basic-{a}-{minMeshSize}-{maxMeshSize}-{curvatureSetting}.stl'

        # Launch the GUI to see the results:
    if '-nopopup' in sys.argv:
        gmsh.fltk.run()

    gmsh.finalize()

    return mesh_name


# mesh(path_basic, mesh_sizes, design_name, surf=False, finger_mesh=False)