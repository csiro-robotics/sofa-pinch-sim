import Sofa
from stlib3.visuals import VisualModel

def Cylinder(name="Cylinder",
                surfaceMeshFileName=None,
                # volumeMeshFileName=None,
                translation=[0., 0., 0.],
                rotation=[0., 0., 0.],
                MOscale = 1.,
                length = 1.,
                uniformScale=1.,
                totalMass=1.,
                volume=1.,
                inertiaMatrix=[1., 0., 0., 0., 1., 0., 0., 0., 1.],
                color=[1., 1., 1., 1.],
                # color=[1., 0., 0., 1.],
                collisionGroup='',
                isAStaticObject=False, 
                parent=None):
    
    
    #### mechanics
    object = Sofa.Core.Node(name)

    if(parent != None):
        parent.addChild(object)

    plugins = ['Sofa.Component.Mapping', 'Sofa.Component.SolidMechanics.Spring']
    object.addObject('MechanicalObject',
                      name="mstate", template="Rigid3",
                      translation2=translation, rotation2=rotation, showObjectScale=MOscale)

    object.addObject('UniformMass', name="mass", vertexMass=[totalMass, volume, inertiaMatrix[:]])


    if not isAStaticObject:
        plugins.append('SofaConstraint')
        plugins.append('SofaImplicitOdeSolver')
        object.addObject('EulerImplicitSolver')
        object.addObject('CGLinearSolver')

    def addCollisionModel(inputMesh=surfaceMeshFileName):
        objectCollis = object.addChild('collision')
        plugins = ['Sofa.Component.Collision.Geometry', 'Sofa.Component.Collision.Detection.Intersection', 
                   'Sofa.Component.Collision.Response.Mapper', 'Sofa.Component.Collision.Response.Contact']
        objectCollis.addObject('RequiredPlugin', pluginName= plugins)
        objectCollis.addObject('MeshSTLLoader', name="loader",
                            filename=inputMesh, triangulate=True,
                            scale=uniformScale)

        objectCollis.addObject('MeshTopology', src="@loader")
        objectCollis.addObject('MechanicalObject')

        if isAStaticObject:
            objectCollis.addObject('TriangleCollisionModel', moving=False, simulated=False, group=collisionGroup)
            objectCollis.addObject('LineCollisionModel', moving=False, simulated=False, group=collisionGroup)
            objectCollis.addObject('PointCollisionModel', moving=False, simulated=False, group=collisionGroup)
        else:
            objectCollis.addObject('TriangleCollisionModel', group=collisionGroup)
            objectCollis.addObject('LineCollisionModel', group=collisionGroup)
            objectCollis.addObject('PointCollisionModel', group=collisionGroup)

        objectCollis.addObject('RigidMapping')

    object.addCollisionModel = addCollisionModel

    #### visualization
    def addVisualModel(inputMesh=surfaceMeshFileName):
        visual = VisualModel(name="visual", visualMeshPath=inputMesh, color=color, scale=[uniformScale]*3)
        object.addChild(visual)
        visual.addObject('RigidMapping')

    object.addVisualModel = addVisualModel

    if surfaceMeshFileName != None:
        object.addCollisionModel()
        object.addVisualModel()

    object.addObject('RequiredPlugin', pluginName=plugins)

    return object