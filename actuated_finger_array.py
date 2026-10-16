import Sofa
from elastic_material_object import ElasticMaterialObject
from stlib3.physics.mixedmaterial import Rigidify
from stlib3.physics.collision import CollisionMesh
from actuated_arm import ActuatedArm
from stlib3.components import addOrientedBoxRoi
import numpy as np
from stlib3.scene import Scene
import matplotlib.pyplot as plt
import sys
from splib3.constants import Key
import os 
import logging

vol_mesh=os.path.join(os.getcwd(), "data/fem-0-1-2-1.msh")

class ActuatedFingerLeft(Sofa.Prefab):
    prefabParameters = [
        {"name": "rotation", "type": "Vec3d", "help": "Rotation in base frame", "default": [90.0, 0.0, 0.0]},
        {"name": "translation", "type": "Vec3d", "help": "Translation in base frame",
         "default": [0.0, 0.0, 0.0]}
    ]

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)

    # Construct the actuated finger
    def init(self):
        # Load the finger mesh and create an elastic body from it
        self.elasticMaterial = self.elasticBody()
        self.ElasticBody.init()

        arm = self.addChild(ActuatedArm(name="ActuatedArmLeft", rotation=[90.0, 0.0, 90.0], translation=[0, 0, 0]))
        arm.ServoMotor.Articulation.dofs.position.value = [[arm.angleIn.value]]  # Initialize the angle
        arm.ServoMotor.minAngle.value = 0
        arm.ServoMotor.maxAngle.value = 0.4

        # Define a ROI to rigidify the nodes of the finger mesh clamped in the servo arm
        box = addOrientedBoxRoi(self,
                                name="boxROIclamped",
                                position=[list(i) for i in self.elasticMaterial.dofs.rest_position.value],
                                translation=[-20e-3, 0e-3, 30.0e-3],  
                                # eulerRotation=[-15.0, 0.0, 90.0],
                                eulerRotation=[10.0, 0.0, 90.0],
                                scale=[60e-3, 45e-3, 40e-3])
        box.drawBoxes = True
        box.init()

        # Get the indices of the finger mesh in the ROI, and the ROI frame
        indices = [ind for ind in box.indices.value]
        frame = [[0, 0, 0, 0, 0, 0, 1]]

        # Rigidify the finger nodes in the ROI. Create a Rigidified object and set up a spring force
        # field to constrain the nodes to stay in the rest shape 把roi里面的元素全部刚度化  取消所有的位移
        rigidifiedStruct = Rigidify(self, self.elasticMaterial, groupIndices=[indices], frames=frame,
                                    name="RigidifiedStructure")

        servoArm = arm.ServoMotor.Articulation.ServoWheel.ServoArm
        servoArm.addChild(rigidifiedStruct.RigidParts)
        servoArm.RigidParts.addObject('RigidRigidMapping', index=0, input=servoArm.dofs.getLinkPath())

        # Add monitoring shouli
        # monitorIndices = [x for x in [ind for ind in self.elasticMaterial.mass.indices.value] if x not in indices]
        # self.elasticMaterial.addObject('Monitor', name='forces', listening='1', indices=monitorIndices, template='Vec3d', 
        #         showForces="True", ForcesColor='1 0 0 1', sizeFactor='5e-2', showMinThreshold='1e-6')

        # Add collision models, to compute collision between the finger and the object,
        # and the inner surfaces of the left and right walls
        self.addCollision()

        
    
    def elasticBody(self):

        # Create a body as a child of the parent (the actuated finger)
        body = self.addChild("ElasticBody")

        # Create an ElasticMaterialObject, which import a mesh, assign it dofs  and mechanical properties
        # The rotation and translation are adjusted so that the mesh is correctly positioned
        e = body.addChild(ElasticMaterialObject(
            volumeMeshFileName=f"data/{sys.argv[2]}",
            #volumeMeshFileName=vol_mesh,
            topoMesh="tetrahedron",
            scale=[1e-3, 1e-3, 1e-3],
            totalMass=0.014697,
            youngModulus=12e6,   #ninjaflex
            poissonRatio=0.45,
            rotation=[90.0, 0.0, 90.0],   #view sofa [y, x, z]
            #translation=[-38.5e-3, 9.5e-3, 20e-3]))
            translation=[0e-3, 0e-3, 50e-3]))

        return e

    def addCollision(self):
 
        # Add a collision model   selfcollision=0 by default
        self.elasticMaterial.addObject('TriangleCollisionModel', simulated='1',contactStiffness='10000', selfCollision='1', group='1', color=[0, 0, 0, 0])

        # Uncomment to use  surface, no entire mesh have contact
        # CollisionMesh(self.elasticMaterial, name='SelfCollisionMesh1',
        #                             surfaceMeshFileName="Data/finger_surface_contact_in1.stl",
        #                             rotation=[90.0, -25.0, 0.0], translation=[-29.5e-3, 19.0e-3, 28.5e-3])



class ActuatedFingerMiddle(Sofa.Prefab):
    prefabParameters = [
        {"name": "rotation", "type": "Vec3d", "help": "Rotation in base frame", "default": [0.0, 0.0, 0.0]},
        {"name": "translation", "type": "Vec3d", "help": "Translation in base frame",
         "default": [0.0, 0.0, 0.0]}
    ]

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)

    # Construct the actuated finger
    def init(self):
        # Load the finger mesh and create an elastic body from it
        self.elasticMaterial = self.elasticBody()
        self.ElasticBody.init()


        arm = self.addChild(ActuatedArm(name="ActuatedArmMiddle", rotation=[90.0, 0, 270.0], translation=[80e-3, 0, 0]))
        arm.ServoMotor.Articulation.dofs.position.value = [[arm.angleIn.value]]  # Initialize the angle
        arm.ServoMotor.minAngle.value = -0.4
        arm.ServoMotor.maxAngle.value = 0


        #固定框的左表
        box = addOrientedBoxRoi(self,
                                name="boxROIclamped",
                                position=[list(i) for i in self.elasticMaterial.dofs.rest_position.value],
                                translation=[100e-3, 0e-3, 30.0e-3],                                     #translation=[110e-3, 0e-3, 20e-3],    
                                eulerRotation=[-10.0, 0.0, 90.0],
                                scale=[60e-3, 45e-3, 40e-3])                                            #scale=[40e-3, 45e-3, 50e-3])
        box.drawBoxes = True
        box.init()

        # Get the indices of the finger mesh in the ROI, and the ROI frame
        indices = [[ind for ind in box.indices.value]]
        frame = [[0, 0, 0, 0, 0, 0, 1]]

        rigidifiedStruct = Rigidify(self, self.elasticMaterial, groupIndices=indices, frames=frame,
                                    name="RigidifiedStructure")

        servoArm = arm.ServoMotor.Articulation.ServoWheel.ServoArm
        servoArm.addChild(rigidifiedStruct.RigidParts)
        servoArm.RigidParts.addObject('RigidRigidMapping', index=0, input=servoArm.dofs.getLinkPath())

        # Add collision models, to compute collision between the finger and the object,
        # and the inner surfaces of the left and right walls
        self.addCollision()

    def elasticBody(self):
        # Create a body as a child of the parent (the actuated finger)
        body = self.addChild("ElasticBody")

    
        e = body.addChild(ElasticMaterialObject(
            volumeMeshFileName=f"data/{sys.argv[2]}",
            #volumeMeshFileName=vol_mesh,
            topoMesh="tetrahedron",
            scale=[1e-3, 1e-3, 1e-3],
            totalMass=0.014697,
            youngModulus=12e6,
            poissonRatio=0.45,
            # rotation=[90.0, -15.0, 120.0],
            rotation=[90.0, 0, -90.0],
            # translation=[36e-3, -55e-3, 7.5e-3]))
            translation=[80e-3, 0e-3, 50e-3]))   #50e-3

        return e

    def addCollision(self):
        # Add a collision model
        self.elasticMaterial.addObject('TriangleCollisionModel', simulated='1', contactStiffness='10000',selfCollision='1', group='1', color=[0, 0, 0, 0])



class FingerController(Sofa.Core.Controller):

    def __init__(self, *args, **kwargs):
        
        # These are needed (and the normal way to override from a python class)
        Sofa.Core.Controller.__init__(self, *args, **kwargs)

        self.node = kwargs["node"]
        self.duration = 2.0
        self.time = 0.0
        self.objectDof = kwargs["objectDof"]
        self.actuator = kwargs["actuator"]
        self.forceContact = 0.0
        self.numContact = 0
        self.surfaceMeshData = True
        self.surfaceMeshData2 = False
        self.endAnimation = False
        self.fitness1_values = []
        self.fitness2_values = []

        # Computation of the contact force applied on the object to grasp
        self.node.getRoot().GenericConstraintSolver.computeConstraintForces.value = True
        
        ### tip indice 找到设计的顶点 然后取最大的displacement
        self.tipIndice = 0
        counter = 0
        highestPoint = -500     

        for i in self.node.getRoot().Modelling.ActuatedFingerLeft.ElasticBody.ElasticMaterialObject.dofs.rest_position.value:
            if i[2] > highestPoint:
                highestPoint = i[2]
                self.tipIndice = counter
            counter += 1

        ####force indice contact surface
        
        if self.surfaceMeshData:
            self.contactSurface = []
            
            self.position = []
            for i in range(0,self.node.getRoot().Modelling.ActuatedFingerLeft.ElasticBody.ElasticMaterialObject.dofs.size.value):
                position2 = self.node.getRoot().Modelling.ActuatedFingerLeft.ElasticBody.ElasticMaterialObject.dofs.position.value[i]
                self.position.append(position2)
            # print('POSITION------------', len(self.position))

            for i in range(0, len(self.position)):
                contactedge=1
                for j in range (0, len(self.position)):
                    if self.position[i][2] < self.position[j][2] and self.position[i][0]<self.position[j][0]:
                        contactedge = 0
                if contactedge:
                    self.contactSurface.append(i)


    def onKeypressedEvent(self, event):
        """
        Using Ctrl+P within the simulation will plot the overall displacement of the mesh contact surface
        """
        key = event['key']
        if key == Key.P:
            print("Plotting")
            dataCurrent = self.currentStates.T
            dataFree = self.freeMotionStates.T
            dataRest = self.restStates.T

            ax = plt.axes(projection = '3d')

            ax.scatter(dataCurrent[0], dataCurrent[1], dataCurrent[2], label="Current")
            ax.scatter(dataFree[0], dataFree[1], dataFree[2], label="Free Motion")
            ax.scatter(dataRest[0], dataRest[1], dataRest[2], label="Rest")
            ax.set_title('Plot of Contact Mesh Positions')
            
            ax.set_aspect('equal')
            plt.legend(loc="upper right")
            plt.show()

    def plotContactDisplacement(self):
        """ Plots the contact displacements """
        dataCurrent = self.currentStates.T
        dataFree = self.freeMotionStates.T
        dataRest = self.restStates.T

        ax = plt.axes(projection = '3d')
        plt.clf()
        ax.scatter(dataCurrent[0], dataCurrent[1], dataCurrent[2], label="Current")
        ax.scatter(dataFree[0], dataFree[1], dataFree[2], label="Free Motion")
        ax.scatter(dataRest[0], dataRest[1], dataRest[2], label="Rest")
        ax.set_title('Plot of Contact Mesh Positions')
        
        ax.set_aspect('equal')
        plt.legend(loc="upper right")
        plt.show(block=False)

    def onAnimateBeginEvent(self,eventType):
        # Print Current Simulation Time
        print("Simulation time is: ", self.time)

        angularStep = 0.04
        angleInit = 0        
        self.time += self.node.dt.value
        angle_data = self.actuator.ServoMotor.angleIn
        angle_out = self.actuator.ServoMotor.angleOut
        angle = angle_data.value
        
       

        if angle < 0.04:
            self.actuator.ServoMotor.angleIn = angleInit + angularStep * self.time / self.duration
            angle_data = self.actuator.ServoMotor.angleIn
            angle = angle_data.value
        else:
            # print('debug', angle)
            self.actuator.ServoMotor.angleIn =  angle
        # self.actuator.ServoMotor.angleOut =  angle

        # Retrieve the Von Mises Stress of the collision mesh
        #vonMisesStressVec = self.node.getRoot().Modelling.ActuatedFingerLeft.ElasticBody.ElasticMaterialObject.forcefield.vonMisesPerElement.value

        # vonMisesStressVec = round(vonMisesStressVec, 3)
        #print("LMaximum Von Mises Stress is: ", max(vonMisesStressVec))  

        # read force on surface
        Lforcesumx = 0
        for i in self.contactSurface:
            
            force = self.node.getRoot().Modelling.ActuatedFingerLeft.ElasticBody.ElasticMaterialObject.dofs.force[i]
            # if force[0] >0.01:
            Lforcesumx += force[0]

        LnormalForce = np.linalg.norm([Lforcesumx])
        # fitness1 = round(LnormalForce,3)
        fitness1 = LnormalForce
        print("Norm of the contact force: " + str(fitness1))
        logging.info(f'Norm of the contact force: {str(LnormalForce)}')


        # Find tip displacement
        a = self.node.getRoot().Modelling.ActuatedFingerLeft.ElasticBody.ElasticMaterialObject.dofs.position[self.tipIndice]
        b = self.node.getRoot().Modelling.ActuatedFingerLeft.ElasticBody.ElasticMaterialObject.dofs.rest_position[self.tipIndice]   #free_position
        tipDisplacement = np.linalg.norm(a-b)
        # fitness2 = round(tipDisplacement,3)
        fitness2 = tipDisplacement
        print("Displacement at the tip: " + str(fitness2))
        logging.info(f'Displacement at the tip: {str(tipDisplacement)}')

        
        self.fitness1_values.append(fitness1)
        self.fitness2_values.append(fitness2)

        return [fitness1, fitness2]

    def get_fitness_values(self):
        return self.fitness1_values, self.fitness2_values
    
    def stopanimation():
        
        pass
    

class FingerController_opporsite(Sofa.Core.Controller):

    def __init__(self, *args, **kwargs):
        # These are needed (and the normal way to override from a python class)
        Sofa.Core.Controller.__init__(self, *args, **kwargs)

        self.node = kwargs["node"]
        # self.duration = 10.0
        self.duration = 2.0
        self.time = 0.0
        self.objectDof = kwargs["objectDof"]
        self.actuator = kwargs["actuator"]
        self.forceContact = 0.0
        self.numContact = 0
        self.surfaceMeshData = True
        

        ####visualize the points that are in contact 接触的点plot

        # Computation of the contact force applied on the object to grasp
        self.node.getRoot().GenericConstraintSolver.computeConstraintForces.value = True
        self.tipIndice = 0
        counter = 0

        ####  finger contact
        highestPoint = -500

        for i in self.node.getRoot().Modelling.ActuatedFingerMiddle.ElasticBody.ElasticMaterialObject.dofs.rest_position.value:
            if i[2] > highestPoint:
                highestPoint = i[2]
                self.tipIndice = counter
            counter += 1

        if self.surfaceMeshData:
            self.contactSurface = []
            self.contactSurface2 = []

            self.position = []
            for i in range(0,self.node.getRoot().Modelling.ActuatedFingerMiddle.ElasticBody.ElasticMaterialObject.dofs.size.value):
                position2 = self.node.getRoot().Modelling.ActuatedFingerLeft.ElasticBody.ElasticMaterialObject.dofs.position.value[i]
                self.position.append(position2)
            # print('POSITION------------', len(self.position))

            for i in range(0, len(self.position)):
                contactedge=1
                for j in range (0, len(self.position)):
                    if self.position[i][2] < self.position[j][2] and self.position[i][0]<self.position[j][0]:
                        contactedge = 0
                if contactedge:
                    self.contactSurface.append(i)

                    
    def onKeypressedEvent(self, event):
        """
        Using Ctrl+P within the simulation will plot the overall displacement of the mesh contact surface
        """
        key = event['key']
        if key == Key.P:
            print("Plotting")
            dataCurrent = self.currentStates.T
            dataFree = self.freeMotionStates.T
            dataRest = self.restStates.T

            ax = plt.axes(projection = '3d')

            ax.scatter(dataCurrent[0], dataCurrent[1], dataCurrent[2], label="Current")
            ax.scatter(dataFree[0], dataFree[1], dataFree[2], label="Free Motion")
            ax.scatter(dataRest[0], dataRest[1], dataRest[2], label="Rest")
            ax.set_title('Plot of Contact Mesh Positions')
            
            ax.set_aspect('equal')
            plt.legend(loc="upper right")
            plt.show()

    def plotContactDisplacement(self):
        """ Plots the contact displacements """
        dataCurrent = self.currentStates.T
        dataFree = self.freeMotionStates.T
        dataRest = self.restStates.T

        ax = plt.axes(projection = '3d')
        plt.clf()
        ax.scatter(dataCurrent[0], dataCurrent[1], dataCurrent[2], label="Current")
        ax.scatter(dataFree[0], dataFree[1], dataFree[2], label="Free Motion")
        ax.scatter(dataRest[0], dataRest[1], dataRest[2], label="Rest")
        ax.set_title('Plot of Contact Mesh Positions')
        
        ax.set_aspect('equal')
        plt.legend(loc="upper right")
        plt.show(block=False)

    def onAnimateBeginEvent(self, eventType):
        # Print Current Simulation Time
        # print("Simulation time is: ", self.time)

        angularStep = 0.04
        angleInit = 0
        self.time += self.node.dt.value

        angle_data = self.actuator.ServoMotor.angleIn
        angle = angle_data.value
        
        # actuation
        if angle < 0.04:
            self.actuator.ServoMotor.angleIn = angleInit + angularStep * self.time / self.duration
            angle_data = self.actuator.ServoMotor.angleIn
            angle = angle_data.value
        else:
            # print('assssssss', angle)
            self.actuator.ServoMotor.angleIn = angle
            # self.endAnimation = True
            # angle = math.pi/3

        
###定义 场景  添加 地板 重力
# def createScene(rootNode):
    

#     # Define the main architecture of the scene, with a node Modelling, Setting and Simulation
#     # Define also the integration method as Euler implicit and the solver as Conjugate Gradient)
#     scene = Scene(rootNode, gravity=[0.0, 0.0, -9.81],
#                   plugins=['SofaSparseSolver', 'SofaOpenglVisual', 'SofaSimpleFem', 'SofaDeformable', 'SofaEngine',
#                            'SofaGeneralRigid', 'SofaRigid', 'SofaBoundaryCondition', 'SofaMeshCollision'],
#                   iterative=False)
#     scene.addMainHeader()

#     # Setting the time step
#     rootNode.dt = 0.01

    
#     # Define the default view of the scene on SOFA
#     scene.addObject('DefaultVisualManagerLoop')
#     scene.VisualStyle.displayFlags = ["showInteractionForceFields", "showForceFields",
#                                       "showCollisionModels"]
#     # Add a grid on the scene with squares 10mm/10mm
#     rootNode.addObject("OglGrid", nbSubdiv=100, size=1)

#     # Set up the pipeline for the collision computation
#     scene.addObject('FreeMotionAnimationLoop')
#     scene.addObject('GenericConstraintSolver', maxIterations=50, tolerance=1e-5)
#     scene.Simulation.addObject('GenericConstraintCorrection')
#     scene.Settings.mouseButton.stiffness = 10

#     # Create one actuated finger
#     actuatedFinger = ActuatedFingerLeft()
#     scene.Modelling.addChild(actuatedFinger)

#     # Add the simulated elements to the Simulation node
#     scene.Simulation.addChild(actuatedFinger.RigidifiedStructure.DeformableParts)
#     scene.Simulation.addChild(actuatedFinger.ActuatedArmLeft)
#     actuatedFinger.ActuatedArmLeft.ServoMotor.Articulation.ServoWheel.ServoArm.dofs.showObject = True
#     actuatedFinger.ActuatedArmLeft.ServoMotor.Articulation.ServoWheel.ServoArm.dofs.showObjectScale = 0.01
#     actuatedFinger.ActuatedArmLeft.ServoMotor.Articulation.ServoWheel.ServoArm.RigidParts.dofs.showObject = True
#     actuatedFinger.ActuatedArmLeft.ServoMotor.Articulation.ServoWheel.ServoArm.RigidParts.dofs.showObjectScale = 0.02

#     # Temporary addition to have the system correctly built in SOFA
#     # Will no longer be required in SOFA v22.12
#     scene.Simulation.addObject('MechanicalMatrixMapper',
#                                name="deformableAndFreeCenterCoupling",
#                                template='Vec1,Vec3',
#                                object1=actuatedFinger.ActuatedArmLeft.ServoMotor.Articulation.dofs.getLinkPath(),
#                                object2=actuatedFinger.RigidifiedStructure.DeformableParts.dofs.getLinkPath(),
#                                nodeToParse=actuatedFinger.RigidifiedStructure.DeformableParts.ElasticMaterialObject.getLinkPath())

    # scene.addObject(FingerController(name='FingerControllerLeft', objectDof=cylObst.collision.MechanicalObject,
    #                                  actuator=scene.Modelling.ActuatedFingerLeft.ActuatedArmLeft, node=rootNode))

