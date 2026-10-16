import sys
import os
import sys
import logging

os.environ['SOFA_ROOT'] = r"C:\Users\SHI178\OneDrive - CSIRO\Documents\Defrost"
os.environ['SOFAPYTHON3_ROOT'] = r'C:\Users\SHI178\OneDrive - CSIRO\Documents\Defrost\plugins\SofaPython3'
sys.path.append(r'C:\Users\SHI178\OneDrive - CSIRO\Documents\Defrost\plugins\SofaPython3\lib\python3\site-packages')
sys.path.append(r'C:\Users\SHI178\OneDrive - CSIRO\Documents\Defrost\plugins\SoftRobots\lib\python3\site-packages')
sys.path.append(r'C:\Users\SHI178\OneDrive - CSIRO\Documents\Defrost\plugins\STLIB\lib\python3\site-packages')
sys.path.append(r'C:\Users\SHI178\OneDrive - CSIRO\Documents\Defrost\plugins\ModelOrderReduction\lib\python3\site-packages')

import Sofa
import Sofa.Gui
from stlib3.scene import Scene
from actuated_finger_array import ActuatedFingerLeft, ActuatedFingerMiddle
from actuated_finger_array import FingerController, FingerController_opporsite
from stlib3.scene.contactheader import ContactHeader
from cylinder import Cylinder
from fixing_box import FixingBox
from stlib3.physics.rigid import Floor, Cube


logging.basicConfig(filename=f'{sys.argv[5]}\Output-mu{sys.argv[3]}-k0{sys.argv[4]}.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)



def main():
   
    # Call the SOFA function to create the root node
    # Call the SOFA function to create the root node
    root = Sofa.Core.Node("root")

    # Call the createScene function, as runSofa does
    createScene(root)

    # Once defined, initialization of the scene graph
    Sofa.Simulation.init(root)
   
    '''
    for iteration in range(250):
        it =str(iteration)
        logging.info(f'iteration number: {it} for the sim associated to param {sys.argv[3]} and {sys.argv[4]}')
        Sofa.Simulation.animate(root, root.dt.value)
        print('*'*50)
        print('iteration number:', iteration)#, ' for the sim associated to param') #, sys.argv[3], sys.argv[4])
    '''
    # Launch the GUI (qt or qglviewer)
    Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1080, 800)
   
    
    # Initialization of the scene will be done here
    Sofa.Gui.GUIManager.MainLoop(root)
    Sofa.Gui.GUIManager.closeGUI()
    
    

def createScene(rootNode):
    

    three_finger = False

    # Define the main architecture of the scene, with a 
    # node Modelling, Setting and Simulation
    # Define also the integration method as Euler implicit and the solver as Conjugate Gradient)

    scene = Scene(rootNode, gravity=[0.0, 9.81, 0],   #m/s^2
                #   plugins=['SofaSparseSolver', 'SofaOpenglVisual', 'SofaSimpleFem', 'SofaDeformable', 'SofaEngine',
                #            'SofaGeneralRigid', 'SofaRigid', 'SofaBoundaryCondition', 'SoftRobots', 
                #            'SofaPython3', 'Sofa.Component.SolidMechanics.FEM.HyperElastic'
                #            ],
                           
                plugins=[ 'SoftRobots', 
                           'SofaPython3'
                           ],
                  iterative=False)

    # Loading all required SOFA modules
    confignode = rootNode.addChild("Config")
    confignode.addObject('RequiredPlugin', name="Sofa.Component.AnimationLoop", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Collision.Detection.Algorithm", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Collision.Detection.Intersection", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Collision.Geometry", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Collision.Response.Contact", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Constraint.Lagrangian.Correction", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Constraint.Lagrangian.Solver", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.IO.Mesh", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.LinearSolver.Iterative", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Mapping.NonLinear", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Mass", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.ODESolver.Backward", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.StateContainer", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Topology.Container.Constant", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Visual", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.GL.Component.Rendering3D", printLog=False)
    confignode.addObject('RequiredPlugin', name = "ArticulatedSystemPlugin")
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.Constraint.Projective")
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.Engine.Select")
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.LinearSolver.Direct")
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.SolidMechanics.FEM.Elastic")
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.Mapping.Linear")  
    #confignode.addObject('RequiredPlugin', name = "Sofa.Component.Mapping.MappedMatrix")
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.SolidMechanics.Spring")
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.Topology.Container.Dynamic")
    #confignode.addObject('RequiredPlugin', name = "Sofa.GUI.Component")
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.SolidMechanics.FEM.HyperElastic")

    confignode.addObject('OglSceneFrame', style="Arrows", alignment="TopRight")
    
    '''confignode = rootNode.addChild("Config")
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Collision", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.AnimationLoop", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.Constraint.Lagrangian.Correction", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.IO.Mesh", printLog=False)
    confignode.addObject('RequiredPlugin', name="ArticulatedSystemPlugin", printLog=False)
    confignode.addObject('RequiredPlugin', name="SofaValidation", printLog=False)
    confignode.addObject('RequiredPlugin', name="Sofa.Component.LinearSolver.Direct", printLog=False)
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.SolidMechanics.FEM.Elastic")
    confignode.addObject('RequiredPlugin', name = "Sofa.Component.Engine.Select")


    confignode.addObject('RequiredPlugin', name="Sofa.GL.Component.Rendering3D", printLog=False)
    confignode.addObject('OglSceneFrame', style="Arrows", alignment="TopRight")
'''

    scene.addMainHeader()

    ContactHeader(scene, alarmDistance=12e-3, contactDistance=1e-3, frictionCoef=0.8)

    
    rootNode.dt = 0.05

    # Define the default view
    scene.addObject('DefaultVisualManagerLoop')
    scene.VisualStyle.displayFlags = ["hideInteractionForceFields", "showForceFields", "showCollisionModels"] #hideInteractionForceFields
       
    # Add a grid on the scene with squares 10mm/10mm
    # rootNode.addObject("OglGrid", nbSubdiv=100, size=1)

    # Set up the pipeline for the collision computation
    # scene.addObject('FreeMotionAnimationLoop')
    # # scene.addObject('EulerImplicitSolver', name='TimeIntegrationSchema')
    # scene.addObject('GenericConstraintSolver', maxIterations=1000, tolerance=1e-5)

    scene.Simulation.addObject('GenericConstraintCorrection')
    scene.Simulation.TimeIntegrationSchema.rayleighStiffness = 1
    scene.Settings.mouseButton.stiffness = 1000   ### moni  mouse tuozhuai 

    # Create one actuated finger
    actuatedFingerLeft = ActuatedFingerLeft()
    if three_finger:
        actuatedFingerMiddle = ActuatedFingerMiddle()
    

    scene.Modelling.addChild(actuatedFingerLeft)
    if three_finger:
        scene.Modelling.addChild(actuatedFingerMiddle)


    # Install an apple in the scene/object to grasp

    scene.Modelling.addChild('Obstacle')

   
    #object_depth = sys.argv[3]
    #print("debug===========", object_depth)

    
    #s_mesh_path = os.path.join(os.getcwd(), 'data', 'apple_new.stl')
    s_mesh_path = os.path.join(os.getcwd(), 'data', 'object' , 'fem-object_4.STEP-4-8-1.stl')

    # define cylinder.py as obsacle and load object file
    # set object to be in the same orientation as objects in gantry (x-y direction) with object base height to fingertip
    cylObst = Cylinder(parent=scene.Modelling.Obstacle, rotation=[270, 0, 90], translation=[0.04, 0.0, 0.115],  #0.115 down 
                        #surfaceMeshFileName=f'data/object/{sys.argv[2]}',
                        surfaceMeshFileName=s_mesh_path,
                        MOscale=10e-3,
                        uniformScale=1e-3,  # uniformlly fangda  suoxiao
                        totalMass=0.232,
                        color=[1., 1., 1., 1.],
                        isAStaticObject=True)
    
    # cylObst.addObject('UncoupledConstraintCorrection')
    
    cylObst.mass.showAxisSizeFactor = 2e-2
    
    # mstate property
    cylObst.mstate.name = 'dofs' 
    
    # Set object base height to tip of the finger
    FixingBox(scene.Modelling.Obstacle, cylObst, translation=[0.04, 0.0, 0.115],
                          scale=[0.05, 0.05, 0.1])
    scene.Modelling.Obstacle.FixingBox.BoxROI.drawBoxes = True


    #----------------------------------------
    # cube = Cube(rootNode,
    #             uniformScale=1e-3,
    #             color=[1.0, 1.0, 0.0, 1.0],
    #             totalMass=0.3,
    #             # volume=20,
    #             # inertiaMatrix=[1000.0, 0.0, 0.0, 0.0, 1000.0, 0.0, 0.0, 0.0, 1000.0],
    #             translation=[0.04, 0.0, object_depth])
    # cube.addObject('UncoupledConstraintCorrection')
    #----------------------------------------



     # Add the simulated elements to the Simulation node 添加软体手指元素给仿真
    scene.Simulation.addChild(actuatedFingerLeft.RigidifiedStructure.DeformableParts)
    scene.Simulation.addChild(actuatedFingerLeft.ActuatedArmLeft)

    if three_finger:
        scene.Simulation.addChild(actuatedFingerMiddle.RigidifiedStructure.DeformableParts)
        scene.Simulation.addChild(actuatedFingerMiddle.ActuatedArmMiddle)

    # Add a controller to output some performance metric during the simulation 输出实验数据
    scene.addObject(FingerController(name='FingerControllerLeft', objectDof=cylObst.collision.MechanicalObject,
                                     actuator=scene.Modelling.ActuatedFingerLeft.ActuatedArmLeft, node=rootNode))

    if three_finger:
        scene.addObject(FingerController_opporsite(name='FingerControllerMiddle', objectDof=cylObst.collision.MechanicalObject,
                                        actuator=scene.Modelling.ActuatedFingerMiddle.ActuatedArmMiddle, node=rootNode))
    
    '''scene.Simulation.addObject('MechanicalMatrixMapper',
                               name="deformableAndFreeCenterCoupling1",
                               template='Vec1,Vec3',
                               object1=actuatedFingerLeft.ActuatedArmLeft.ServoMotor.Articulation.dofs.getLinkPath(),
                               object2=actuatedFingerLeft.RigidifiedStructure.DeformableParts.dofs.getLinkPath(),
                               nodeToParse=actuatedFingerLeft.RigidifiedStructure.DeformableParts.ElasticMaterialObject.getLinkPath())

    if three_finger:
        scene.Simulation.addObject('MechanicalMatrixMapper',
                                name="deformableAndFreeCenterCoupling2",
                                template='Vec1,Vec3',
                                object1=actuatedFingerMiddle.ActuatedArmMiddle.ServoMotor.Articulation.dofs.getLinkPath(),
                                object2=actuatedFingerMiddle.RigidifiedStructure.DeformableParts.dofs.getLinkPath(),
                                nodeToParse=actuatedFingerMiddle.RigidifiedStructure.DeformableParts.ElasticMaterialObject.getLinkPath())'''


#/mesh/fem-0-1-2-1.msh object_15.stl 0.145015979865033 /mesh/basic-0-1-2-1.stl

if __name__ == '__main__':
    main()
