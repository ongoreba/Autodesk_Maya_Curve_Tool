import maya.cmds as cmds

RED =       [1.0,0.0,0.0]
GREEN =     [0.0,1.0,0.0]
BLUE =      [0.0,0.0,1.0]

PRESET_SQUARE = 'square'

##############################################################################################

def create( name = 'curve', preset = 'square', size = 1, parent = None, color = None ):

    """Create a New Curve Control
            RETURN    Name of the New Curve
    name    <str>     Name of the new CURVE that is Created
    preset  <str>     TYPE of Curve to Create
                        square | triangle | ...
    size    <float>   Size of the new Curve
    parent  <str>
    """
    if preset == 'triangle':
        # DEFINE a TRIANGLE curve
        points =    [(-1,0,-1),
                    (1, 0, -1),
                    (0,0,1),
                    (-1,0,-1)]
        knots = [0,1,2,3]
        degree = 1
    
    else:
        points =    [(-1,0,-1),
                    (1, 0, -1),
                    (1,0,1),
                    (-1,0,1),
                    (-1,0,-1)]
        knots = [0,1,2,3,4]
        degree = 1
    
    #RESIZE the CURVE POINTS
    resizedPoints = []
    for point in points:
        resizedPoint = [point[0]*size, point[1]*size, point[2]*size]
        resizedPoints.append( resizedPoint )
    
    # CREATING the CURVE
    nuCurve = cmds.curve ( point = resizedPoints, knot = knots, degree = 1 )
    
    # RENAME the CURVE
    nuCurve = cmds.rename ( nuCurve, name )
    
    # REPARENT ?
    if parent is not None and cmds.objExists(parent):
        nuCurve = cmds.parent( nuCurve, parent )[0]
    
    # Colorize the CURVE
    if color is not None :
        cmds.color( nuCurve, rgb = color )
    
    # RETURN the CURVE NAME
    return nuCurve
    


##############################################################################################
def doTool( targets = None, preset = 'square', suffix = 'ctrl', color = None ):
    """Interactive Curve Creating TOOL
    
    targets     <(str)>     List of Nodes to create a Curve For...
                <bool>      If TRUE, Create a Curve for everything in the Scene Selection.
    
    """
    result = []
    # Validate Our TARGETS
    if targets is True:
        # WE are going to get the CURRENT SELECTION
        targets = cmds.ls( selection = True )
    elif isinstance(targets, str):
        targets = [targets]
        
    if not isinstance( targets, list):
        print("IMPROPER Targets Supplied!!!")
        return result
    
    
    
    
    if targets is not None:
        for target in targets:
            if not (isinstance(target, str) and cmds.objExists(target) ):    #isinstance findinf statement
                print("TARGET does not existed!!!", target)
                continue
            #Get the SHAPE...
            shapes = cmds.listRelatives(target, shapes = True, path = True )
            # DETERMINE a Good Size for the Curve
            size = 1
            if shapes is not None:
                shape = shapes [0]
                # BOUNDING BOX is a list [xSize, ySize, zSize]
                bbSize = cmds.getAttr( shape + '.boundingBoxSize' )
                size = bbSize[0][0]    # USE the xSize
                size = size/2.0         # USE half the Size
        
            nuCurve =   create( name = target + suffix,
                                preset = preset,
                                size = size,
                                parent = None,
                                color = color )
            
            cmds.matchTransform( nuCurve, target )
            result.append(nuCurve)
            
    return result


##############################################################################################

def createFKChain( numberOfControls = 1, length = 10, nestChildControls = False,
                   name = 'curve', preset = 'square', size = 1, parent = None, color = None ):
    result = []
    
    if numberOfControls < 1:
        print ("Need to have a MINIMUM of 1 Control to build")
        return result
    
    # NOW, we  can ITERATE (LOOP) and CREATE a Control until we reach the numberOfControls
    current_x_value = 0
    #To indicate the start number
    
    if numberOfControls > 1:
        delta_x = length / (numberOfControls-1)
    else:
        delta_x = 0 # set delta as at 0
        
    
    current_parent = parent
    for i in range(numberOfControls):
        new_curve = create( name = name, preset = preset, size = size, parent = current_parent, color = color )
        result.append ( new_curve )
        # POSITION the NEW CURVE
        cmds.setAttr (new_curve + ".translateX", current_x_value )
        if nestChildControls == True:
            current_x_value = delta_x
            # UPDATE the Current Parent
            current_parent = new_curve # parenting the curve child
        else:
            current_x_value = current_x_value + delta_x

        
    
    return result
    
def createWireRig( numberOfControls = 4, length = 10, nestChildControls = False,
                   name = 'wire', 
                   Ctrlpreset = 'square', Ctrlsize = 1, Ctrlcolor = None ):
    #VALIDATE THE NUMBER OF CONTROL

    numberOfControls = max( 4 , numberOfControls)

    # CREATE OUR ROOT GROUP

    root = cmds.createNode ('transform')
    root = cmds.rename ( root, name + "_root")


    controls = createFKChain ( numberOfControls = numberOfControls, length = length, nestChildControls = nestChildControls,
                   name = name, preset =  Ctrlpreset, size = Ctrlsize, parent = root, color = Ctrlcolor )

    # CREATE A WIRE CURVE

    '''points = []
    for i in range (numberOfControls):
        point = [ i , 0 ,0 ]
        points.append ( point )'''

    points = [ [ i ,0 , 0] for i in range (numberOfControls)]

    knots = _getKnots (count = numberOfControls , closed = False, degree = 3)
    degrees = 3

    wireCurve = cmds.curve ( point = points, knot = knots, degree = degrees )
    wireCurve = cmds.rename (wireCurve , name + "_wire")

    wireCurve = cmds.parent (wireCurve , root)[0]

    # CONNECT THE CONTROL TO THE WIRE
    for i in range (numberOfControls):
        control = controls[i]

        shapes = cmds.listRelatives (wireCurve , shapes = True , fullPath = True)
        wireShape = shapes[0]

        # MAKE THE LOGIC OF 

        # MULTIPLY MATRIX
        multMatrix = cmds.createNode ("multMatrix")
        
        cmds.connectAttr ( control + ".worldMatrix[0]" , multMatrix + ".matrixIn[0]" , force = True)
        cmds.connectAttr ( wireCurve + ".worldInverseMatrix[0]" , multMatrix + ".matrixIn[1]" , force = True)

        decomposeMatrix = cmds.createNode ("decomposeMatrix")
        decomposeMatrix = cmds.rename()

        cmds.connectAttr ( multMatrix + ".matrixSum", decomposeMatrix + ".inputMatrix" , force = True)

        cmds.connectAttr ( decomposeMatrix + ".outputTranslate" , wireShape + ".controlPoints[" + str(i) + "]", force = True)


def _getKnots(count, closed, degree):
    """Returns the proper Knot Array given the Number of Points, if its closed and the Degree."""
    knots =                                                 []
    if degree == 1:    #LINEAR
        for i in range(count):
            knots.append                                    (i)
    else:            #CUBIC
       
        if closed:
            knots.append                                    (-2)
            knots.append                                    (-1)
            for i in range(count):
                knots.append                                (i)
        else:
            knots.append                                    (0)
            knots.append                                    (0)
            for i in range(count-2):
                knots.append                                (i)
            knots.append                                    (count-3)
            knots.append                                    (count-3)
    return                                                    knots
    