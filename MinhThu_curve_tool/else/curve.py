import maya.cmds as cmds

RED = [1.0, 0.0, 0.0]
GREEN = [0.0, 1.0, 0.0]
BLUE = [0.0, 0.0, 1.0]

PRESET_CIRCLE = "circle"
PRESET_SQUARE = "square"
PRESET_CUBE = "cube"
print (PRESET_SQUARE)
degrees = 1
points = []  # Assign an empty list as default
knots = []
########################################################
def createCurveCtrl(name="curve", preset=PRESET_SQUARE, size=1, parent=None, color=None):

    """Create a New Curve Ctrl
    Args:
        name (str): The name of the base new curve to be created. 
            Default: curve
        preset (str): The type of curve to create.
            Default: PRESET_SQUARE
            Valid values: PRESET_CIRCLE, PRESET_SQUARE, PRESET_CUBE
        size (int): Factor to scale the created curve by.
            Default: 1
        parent (str|None): Name of the object to parent the curve too.
            Default: None
        color (list|None): A list containing 3 floats for RGB values or None.
            Default: None
    Returns:
      str: The name of the newly created curve.
  """
                
    if preset == PRESET_CIRCLE:
        center = (0, 0, 0)
        normal = (0, 1, 0)
        sweep = 360
        radius = 1*size
        degree = 3
        sections = 10

        newCurveCtrl = cmds.circle(
            center = center,
            normal = normal,
            sweep = sweep,
            radius = radius,
            degree = degree,
            useTolerance = False,
            sections = sections,
            constructionHistory = False
            )[0]
    else:
        if preset == PRESET_SQUARE:
            degrees = 1
            points = [
                (-1, 0, -1), (1, 0, -1), (1, 0, 1), 
                (-1, 0, 1), (-1, 0, -1)
                ]
            knots = [0, 1, 2, 3, 4]
        elif preset == PRESET_CUBE:
            degrees = 1
            points = [
                (-1, 1, 1), (1, 1, 1), (1, -1, 1), 
                (-1, -1, 1), (-1, 1, 1), (-1, 1, -1), 
                (-1, -1, -1), (-1, -1, 1), (1, -1, 1), 
                (1, -1, -1), (-1, -1, -1), (-1, 1, -1), 
                (1, 1, -1), (1, -1, -1), (1, 1, -1), 
                (1, 1, 1)
                ]
            knots = (
                0, 1, 2, 3, 4, 5, 6, 7, 8, 
                9, 10, 11, 12, 13, 14, 15
                ) 
        resizedPoints = []

        for point in points:
            resizedPoint = [point[0]*size, point[1]*size, point[2]*size]
            resizedPoints.append(resizedPoint)
        newCurveCtrl = cmds.curve(point=resizedPoints, knot=knots, degree=degrees)

    newCurveCtrl = cmds.rename(newCurveCtrl, name)

    # REPARENT IF THE PARENT IS NOT NONE
    if parent is not None and cmds.objExists(parent):
        newCurveCtrl = cmds.parent(newCurveCtrl, parent)[0]
    # Colorize the curve
    if color is not None:
        cmds.color(newCurveCtrl, rgb=color)

    return(newCurveCtrl)
     

def createCurveFromSelection(selectedObjects=None, suffix="Ctrl", preset=PRESET_SQUARE):

    """Interactive curve creating tool
    Args:
    selectedObjects (list|str): List of Nodes to create a curve for.
        Default: None
    suffix="Ctrl", 
    preset= square

               <bool>    if True, create a  curve for everything selected in the scene """
     

     
    # Validate our selectedObjects
    # If selectedObjects is True or selectedObjects is None:
    curveResult = []
    if selectedObjects is True: # or selectedObjects is None:
        #We are going to get the current selection
        selectedObjects = cmds.ls(selection=True)
    elif isinstance(selectedObjects, str):
        selectedObjects = [selectedObjects]
    if not isinstance(selectedObjects, list):
        cmds.warning("Please have something selected")
        return curveResult
     
    if selectedObjects is not None:
        for selectedObject in selectedObjects:
            if not(isinstance(selectedObject, str) and cmds.objExists(selectedObject)):
                print("There is no selected object", selectedObject)
                continue
            # Get the Shape node of the curve
            selectedShapes = cmds.listRelatives(selectedObject, shapes=True, path=True)
            # Determine a good size for the curve
            size = 1
            if selectedShapes is not None:
                shape = selectedShapes[0]
                # Bounding box size is a list of [xSize . ySize , zSize]
                bbSize = cmds.getAttr(shape +".boundingBoxSize" )
                size = bbSize[0][0]  # Use the xSize
                print (size)
                size = size/2.0  # Use half the size
            newCurveCtrl = createCurveCtrl (
                name="curve", preset=preset+suffix, 
                size=size, parent=None, color=BLUE, 
                )
            cmds.matchTransform(newCurveCtrl, selectedObject)
            curveResult.append(newCurveCtrl)
    return curveResult


def createFkChain(
        numCtrl=1, length=10, nestChildCtrl=False,
        name="curve", preset=PRESET_SQUARE, size=1, parent=None, color=None
        ):
     
    result = []
    if numCtrl<1:
        print("Need to have at least 1 conrol to it")
        return result
    # NOW WE CAN ITERATE (LOOP) and create a control until we reach the numCtrl
    current_x_value = 0
    if numCtrl > 1:
        delta_x = length/(numCtrl - 1)
    else:
        delta_x = 0

    currentParent = parent
    for i in range(numCtrl):
        new_Curve = createCurveCtrl(
            name=name, preset=preset, size=size, 
            parent=currentParent, color=color
            )
        result.append(new_Curve)
        # POSITION THE NEW CURVE 
        cmds.setAttr(new_Curve+".translateX", current_x_value)
        if nestChildCtrl is True:
            currentParent = new_Curve
            current_x_value = delta_x
        else:
            current_x_value = current_x_value+delta_x

    return result


def createWireRig(numCtrl=4, length=10, nestChildCtrl=False, 
                  name='wire', Ctrlpreset=PRESET_SQUARE, 
                  Ctrlsize=1, Ctrlcolor=None
        ):
    #VALIDATE THE NUMBER OF CONTROL

    numCtrl = max(4, numCtrl)

    # CREATE OUR ROOT GROUP

    root = cmds.createNode('transform')
    root = cmds.rename(root, name+"_root")


    controls = createFkChain(numCtrl=numCtrl, 
                             length=length, 
                             nestChildCtrl=nestChildCtrl,
                             name=name, 
                             preset=Ctrlpreset, 
                             size=Ctrlsize, 
                             parent=root, 
                             color=Ctrlcolor )

    # CREATE A WIRE CURVE

    '''points = []
    for i in range (numCtrl):
        point = [ i , 0 ,0 ]
        points.append ( point )'''

    points = [[i, 0, 0] for i in range(numCtrl)]

    knots = _getKnots(count=numCtrl, closed=False, degree=3)
    degrees = 3

    wireCurve = cmds.curve(point = points, knot = knots, degree = degrees)
    wireCurve = cmds.rename(wireCurve, name+"_wire")
    wireCurve = cmds.parent(wireCurve, root)[0]

    # CONNECT THE CONTROL TO THE WIRE
    for i in range(numCtrl):
        control = controls[i]

        shapes = cmds.listRelatives(wireCurve, shapes = True, fullPath = True)
        wireShape = shapes[0]

        # MAKE THE LOGIC OF 

        # MULTIPLY MATRIX
        multMatrix = cmds.createNode("multMatrix")
        multMatrix = cmds.rename(multMatrix, control+"_MULT")
        
        cmds.connectAttr(control+".worldMatrix[0]", multMatrix+".matrixIn[0]", force=True)
        cmds.connectAttr(wireCurve+".worldInverseMatrix[0]", multMatrix+".matrixIn[1]", force=True)

        decomposeMatrix = cmds.createNode("decomposeMatrix")
        decomposeMatrix = cmds.rename(decomposeMatrix, control+"_DEC")

        cmds.connectAttr(multMatrix+".matrixSum", decomposeMatrix+".inputMatrix", force=True)

        cmds.connectAttr(decomposeMatrix+".outputTranslate", wireShape+".controlPoints["+str(i)+"]", force=True)

# rebuild curve 


def _getKnots(count, closed, degree):
    """Returns the proper Knot Array given the Number of Points, if its closed and the Degree."""
    knots = []
    if degree == 1:  # LINEAR
        for i in range(count):
            knots.append(i)
    else:  # CUBIC
       
        if closed:
            knots.append(-2)
            knots.append(-1)
            for i in range(count):
                knots.append(i)
        else:
            knots.append(0)
            knots.append(0)
            for i in range(count-2):
                knots.append(i)
            knots.append(count-3)
            knots.append(count-3)
    return knots
    