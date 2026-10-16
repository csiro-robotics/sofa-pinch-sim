import os
import Sofa
from stlib3.scene import Scene

dirPath = os.path.dirname(os.path.abspath(__file__)) + '/'


class ServoMotor(Sofa.Prefab):
    """An actuator to dirve the fin ray 

    Example 

    def addScene(root):
        ...
        servo = ServoMotor(root)

        ## Direct access to the components
        servo.angle.value = 1.0
    """
    prefabParameters = [
        {'name': 'rotation', 'type': 'Vec3d', 'help': 'Rotation', 'default': [0.0, 0.0, 0.0]},
        {'name': 'translation', 'type': 'Vec3d', 'help': 'Translation', 'default': [0.0, 0.0, 0.0]},
        {'name': 'scale3d', 'type': 'Vec3d', 'help': 'Scale 3d', 'default': [1.0e-3, 1.0e-3, 1.0e-3]}]

    prefabData = [
        {'name': 'minAngle', 'help': 'min angle of rotation (in radians)', 'type': 'float', 'default': -100},
        {'name': 'maxAngle', 'help': 'max angle of rotation (in radians)', 'type': 'float', 'default': 100},
        {'name': 'angleIn', 'help': 'angle of rotation (in radians)', 'type': 'float', 'default': 0},
        {'name': 'angleOut', 'help': 'angle of rotation (in degree)', 'type': 'float', 'default': 0}
    ]

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)

    def init(self):
  
        servoBody = self.addChild('ServoBody')
        servoBody.addObject('MechanicalObject', name='dofs', template='Rigid3', position=[[0., 0., 0., 0., 0., 0., 1.]],
                            translation=list(self.translation.value), rotation=list(self.rotation.value),
                            scale3d=list(self.scale3d.value))
        
        servoBody.addObject('FixedConstraint', indices=0)
        servoBody.addObject('UniformMass', totalMass=0.01)

        visual = servoBody.addChild('VisualModel')
        visual.addObject('MeshSTLLoader', name='loader', filename='data/cylinder.stl', scale=1e-6,  #cylinder-finger SG90_servomotor_finger
                         rotation=[0.0, -90.0, 0.0], translation=[-12.0e-3, -5.0e-3, 0])
        visual.addObject('MeshTopology', src='@loader')
        visual.addObject('OglModel', color=[0.15, 0.45, 0.75, 0.7], writeZTransparent=True)
        visual.addObject('RigidMapping', index=0)

        
        angle = self.addChild('Articulation')
        angle.addObject('MechanicalObject', name='dofs', template='Vec1', position=[[self.getData('angleIn')]],
                        rest_position=self.getData('angleIn').getLinkPath())
        angle.addObject('RestShapeSpringsForceField', points=0, stiffness=1e9)
        angle.addObject('UniformMass', totalMass=0.01)

        servoWheel = angle.addChild('ServoWheel')
        servoWheel.addObject('MechanicalObject', name='dofs', template='Rigid3',
                             position=[[0., 0., 0., 0., 0., 0., 1.], [0., 0., 0., 0., 0., 0., 1.]],
                             translation=list(self.translation.value), rotation=list(self.rotation.value),
                             scale3d=list(self.scale3d.value))
                             
        servoWheel.addObject('ArticulatedSystemMapping', input1="@../dofs", input2="@../../ServoBody/dofs",
                             output="@./")

        articulationCenter = angle.addChild('ArticulationCenter')
        articulationCenter.addObject('ArticulationCenter', parentIndex=0, childIndex=1, posOnParent=[0., 0., 0.],
                                     posOnChild=[0., 0., 0.])
        articulation = articulationCenter.addChild('Articulations')

        articulation.addObject('Articulation', translation=True, rotation=False, rotationAxis=[0, 0, 1],
                               articulationIndex=0)
        
        angle.addObject('ArticulatedHierarchyContainer', printLog=False)

        # The output
        self.angleOut.setParent(angle.dofs.position)


def createScene(rootNode):
    import math
    from splib3.animation import animate

    def animation(target, factor):
        target.angleIn.value = math.sin(factor * 2 * math.pi)

    scene = Scene(rootNode, plugins=['SofaConstraint', 'SofaGeneralRigid', 'SofaOpenglVisual', 'SofaRigid'],
                  iterative=False)
    scene.addMainHeader()
    scene.addObject('DefaultVisualManagerLoop')
    scene.addObject('FreeMotionAnimationLoop')
    scene.addObject('GenericConstraintSolver', maxIterations=1e3, tolerance=1e-5)
    scene.Simulation.addObject('GenericConstraintCorrection')

    scene.dt = 0.01
    scene.gravity = [0., -9810., 0.]

    scene.Simulation.addChild(ServoMotor(name="ServoMotor"))
    animate(animation, {'target': scene.Simulation.ServoMotor}, duration=5., mode='loop')
    scene.Simulation.ServoMotor.Articulation.ServoWheel.dofs.showObject = True
    scene.Simulation.ServoMotor.Articulation.ServoWheel.dofs.showObjectScale = 2e-2

    return scene
