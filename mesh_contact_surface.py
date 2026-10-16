# Script for the generation of internal contact surfaces in the soft finger
# The surface depends on some of the finger's design parameters

import gmsh
import sys

def define_parameters():
    mm = 1e-3
    ea1 = 8.0 * mm
    ea2 = 4.0 * mm
    La = 6.0 * mm
    la = 40.0 * mm
    inter = 15.2 * mm
    rHole = 1.7 * mm
    return ea1, ea2, La, la, inter, rHole

def gen_contact_surface():
    # Definition of variables
    mm = 1e-3

    # ## Design parameters to be varied ## #
    L = 100.0 * mm
    l = 40.0 * mm
    e1 = 8.0 * mm
    e2 = 5.0 * mm
    e3 = 4.0 * mm

    n = 4
    d = [28. * mm, 28. * mm, 28.0 * mm, 28.0 * mm]

    ######################################

    # Thickness of the finger / length of extrusion
    w = 18.0 * mm
    # Length of mesh elements
    lc = 1 * mm


    ea1, ea2, La, la, inter, rHole = define_parameters()

    # Before using any functions in the Python API, Gmsh must be initialized:
    gmsh.initialize()

    # Create a model for the finger surface contact 1
    gmsh.model.add("finger_contact_surface_in1_small")

    gmsh.model.occ.addPoint(ea1, 0, 0, lc, 1)
    gmsh.model.occ.addPoint(e1, L - e2, 0.003, lc, 2)
    gmsh.model.occ.addPoint(e1, L - e2, w - 0.003, lc, 3)
    gmsh.model.occ.addPoint(ea1, 0, w, lc, 4)

    # Draw lies between the points
    for k in range(1, 4):
        gmsh.model.occ.addLine(k, k + 1, k)
    gmsh.model.occ.addLine(4, 1, 4)

    # Define the contour
    gmsh.model.occ.addCurveLoop(range(1, 5), 1)

    # Create the surface delimited by the contour
    surf = gmsh.model.occ.addPlaneSurface([1])

    gmsh.model.occ.synchronize()

    # We finally generate and save the mesh
    gmsh.model.mesh.generate(1)
    # gmsh.write("Data/finger.stl")

    # gmsh.model.mesh.generate(2)

    gmsh.option.setNumber("Mesh.MeshSizeMin", 0.001)
    gmsh.option.setNumber("Mesh.MeshSizeMax", 1)

    gmsh.write("Data/finger_surface_contact_in1_small.stl")

    # Need to synchronize with Gmsh for it to create the desired data structures
    gmsh.model.occ.synchronize()

if __name__ == "__main__":
    gen_contact_surface()