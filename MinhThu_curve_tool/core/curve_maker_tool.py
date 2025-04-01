import maya.cmds as cmds
import logging as log
#import .curve_presets as CP
from .curve_presets import *
from .curve_presets import SHAPE_PRESETS

RED = [1.0, 0.0, 0.0]
GREEN = [0.0, 1.0, 0.0]
BLUE = [0.0, 0.0, 1.0]

degrees = 1
points = []  # Assign an empty list as default
knots = []

def createCurveCtrl(name="curve", 
                    preset=PRESET_SQUARE, 
                    size=1, parent=None, 
                    color=None):

    """Create a New Curve Ctrl
    Args:
        name (str): The name of the base new curve to be created. 
            Default: curve
        preset (str): The type of curve to create.
            Default: "square"
            Valid values:   "circle",
                            "square",
                            "cube",
                            "cog",
                            "arrow",
                            "arrow_cube",
                            "arrow_triangle",
                            "triangle"
        size (int): Factor to scale the created curve by.
            Default: 1
        parent (str|None): Name of the object to parent the curve too.
            Default: None
        color (list|None): A list containing 3 floats for RGB values.
            Default: None
    Returns:
      str: The name of the newly created curve.
    """
    # If the preset is circle
    if preset == PRESET_CIRCLE: #SPECIAL CASE
        center = (0, 0, 0)
        normal = (0, 1, 0)
        sweep = 360
        radius = 1*size
        degree = 3
        sections = 10
        # Make a circle curve
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
    # If not, get all the presets from the SHAPE_PRESETS
    else: 
        # IF an Invalid Preset is Supplied... use the default Square
        """if preset not in SHAPE_PRESETS:
            print ("Invalid Preset: {0}\nUsing Square".format(preset) )
            preset = PRESET_SQUARE   """                               
        shape_data = SHAPE_PRESETS.get(preset)
        degrees = shape_data.get('degrees')
        points = shape_data.get('points')
        knots = shape_data.get('knots')
        
        # Resize the points of the curve
        # Assign an empty list first
        resizedPoints = []
        # For each of those points:
        for point in points:
            # Put them in a list
            # And multiply them to the size
            resizedPoint = [
                point[0]*size, 
                point[1]*size, 
                point[2]*size
            ]            
            resizedPoints.append(resizedPoint)
        # Create a new curve
        newCurveCtrl = cmds.curve(
            point=resizedPoints, 
            knot=knots, 
            degree=degrees
            )

    # Rename the curve
    newCurveCtrl = cmds.rename(newCurveCtrl, name)

    # REPARENT IF THE PARENT IS NOT NONE
    if parent is not None and cmds.objExists(parent):
        newCurveCtrl = cmds.parent(newCurveCtrl, parent)[0]
    # Colorize the curve
    if color is not None:
        cmds.color(newCurveCtrl, rgb=color)
    return(newCurveCtrl)
     
def doGroupSelected(checked=False):
    if checked:
        cmds.group()
    else:
        pass

def createCurveFromSelection(
        selectedObjects=None, 
        suffix="_Ctrl", 
        preset=PRESET_SQUARE
        ):
    """Interactive curve creating tool from selection
    Args:
        selectedObjects (list|str|bool): List of Nodes to create 
                                         a curve for.
                                         If 'is True', create a 
                                         curve for everything 
                                         selected in the scene.
            Default: None
        suffix (str): Name suffix of the curves that get created.
            Default: "Ctrl"
        preset (str): The type of curve to create.
            Default: "square"
            Valid values:   "circle",
                            "square",
                            "cube",
                            "cog",
                            "arrow",
                            "arrow_cube",
                            "triangle"
    Returns:
    curveResult (list): list of the curves being created
    """  
    # Validate our selectedObjects
    # If selectedObjects is True or selectedObjects is None:
    curveResult = []
    if selectedObjects is True: # or selectedObjects is None:
        # We are going to get the current selection
        selectedObjects = cmds.ls(selection=True)
        print(selectedObjects)
    # If there is only one selected object (a string)
    elif isinstance(selectedObjects, str):
        #put them in a list
        selectedObjects = [selectedObjects]
    # If there aren't any selected objects
    if not isinstance(selectedObjects, list) or len(selectedObjects) == 0 :
        cmds.warning("Please have something selected")
        return curveResult
#    if selectedObjects is False:
#        cmds.warning("Please have something selected")
#        return curveResult
 #        
 #   if selectedObjects is not None:
    else:
        for object in selectedObjects:
            """if not(
                isinstance(object, str) and cmds.objExists(object)
                ):
                print("There is no selected object", object)
                continue"""
            # Get the Shape node of the curve
            """selectedShapes = cmds.listRelatives(
                object, 
                shapes=True, 
                path=True
                )"""
            # Determine a good size for the curve
            size = 1
            #if selectedShapes is not None:
            if selectedObjects is not None:
                #shape = selectedShapes[0]
                # Bounding box size is a list of [xSize . ySize , zSize]
                #bbSize = cmds.getAttr(shape +".boundingBoxSize" )
                bbSize = cmds.exactWorldBoundingBox(calculateExactly=True)
                print(bbSize)
                #size = bbSize[0][0]  # Use the xSize
                size = max(bbSize)
                print(size)
                size = size*1.2  # Use almost half the size
            newCurveCtrl = createCurveCtrl (
                name="curve"+suffix, preset=preset, 
                size=size, parent=None, color=RED
                )
            cmds.matchTransform(newCurveCtrl, object, scale=False)
            curveResult.append(newCurveCtrl)
    return curveResult


def createFkChain(
        numCtrl=1, 
        length=10, 
        nestChildCtrl=False,
        name=PRESET_SQUARE, 
        preset=PRESET_SQUARE, 
        size=1, 
        parent=None, 
        color=None
        ):
    """Create a chain consists of Fk controls
        Args:
            numCtrl (int): Number of controls needed for the ribbon.
                          Minimum is 4.
                Default: 4
            length (int|float): Length of the Fk chain
                Default: 10
            nestChildCtrl (bool): Are the controls parented in a hierachy?
                Default: False
            name (str): Name of the control
                Default: "square"
            preset (str): The curve's shape preset
                Default: "square"
                Valid values:   "circle",
                                "square",
                                "cube",
                                "cog",
                                "arrow",
                                "arrow_cube",
                                "arrow_triangle",
                                "triangle"
            size (int|float): Curve's size
                Default: 1
            parent (str): Specify the parent of the Fk chain
                Default: None
            color (str): Color of the curve
                Default: None
                Valid values:   "RED", 
                                "GREEN", 
                                "BLUE"
        Returns:
            result (list): A list of newly created curves
    """
    result = []
    # If the number of control is less than 1
    if numCtrl<1:
        # Tell the user to have at least 1 control
        log.warning("Need to have at least 1 conrol to it")
        return result
    # If the number of controls is more than 1
    current_x_value = 0
    if numCtrl > 1:
        # Find the length of the x axis in world space
        # start from the center of the world
        delta_x = length/(numCtrl - 1)
    else:
        delta_x = 0

    # Now iterate and create a control until we reach the numCtrl
    currentParent = parent
    for i in range(numCtrl):
        newCurve = createCurveCtrl(
            name=name, preset=preset, size=size, 
            parent=currentParent, color=color
            )
        result.append(newCurve)
        # POSITION THE NEW CURVE 
        cmds.setAttr(newCurve+".translateX", current_x_value)
        #
        if nestChildCtrl is True:
            currentParent = newCurve
            current_x_value = delta_x
        else:
            current_x_value = current_x_value+delta_x

    return result


def createRibbonRig(
        numCtrl=4, 
        length=10, 
        nestChildCtrl=False, 
        name='wire', 
        ctrlPreset=PRESET_SQUARE, 
        ctrlSize=1, 
        ctrlColor=None
        ):
    #VALIDATE THE NUMBER OF CONTROL
    """Create a ribbon rig from scratch
        Args:
            numCtrl (int): Number of controls needed for the ribbon.
                          Minimum is 4.
                Default: 4
            length (int|float): Length of the Fk chain
                Default: 10
            nestChildCtrl (bool): Are the controls parented in a hierachy?
                Default: False
            name (str): Name of the control
                Default: "square"
            ctrlPreset (str): The curve's shape preset
                Default: "square"
                Valid values:   "circle",
                                "square",
                                "cube",
                                "cog",
                                "arrow",
                                "arrow_cube",
                                "arrow_triangle",
                                "triangle"
            ctrlSize (int|float): Curve's size
                Default: 1
            ctrlColor (str): Color of the curve
                Default: None
                Valid values:   "RED", 
                                "GREEN", 
                                "BLUE"
    """
    numCtrl = max(4, numCtrl)

    # CREATE OUR ROOT GROUP

    root = cmds.createNode('transform')
    root = cmds.rename(root, name+"_root")


    controls = createFkChain(numCtrl=numCtrl, 
                             length=length, 
                             nestChildCtrl=nestChildCtrl,
                             name=name, 
                             preset=ctrlPreset, 
                             size=ctrlSize, 
                             parent=root, 
                             color=ctrlColor )

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
        
        cmds.connectAttr(
            control+".worldMatrix[0]", 
            multMatrix+".matrixIn[0]", 
            force=True
            )
        cmds.connectAttr(
            wireCurve+".worldInverseMatrix[0]", 
            multMatrix+".matrixIn[1]", 
            force=True
            )

        decomposeMatrix = cmds.createNode("decomposeMatrix")
        decomposeMatrix = cmds.rename(decomposeMatrix, control+"_DEC")

        cmds.connectAttr(
            multMatrix+".matrixSum", 
            decomposeMatrix+".inputMatrix", 
            force=True
            )

        cmds.connectAttr(
            decomposeMatrix+".outputTranslate", 
            wireShape+".controlPoints["+str(i)+"]", 
            force=True
            )


def _getKnots(count, closed, degree):
    """Returns the proper Knot Array given the Number of Points, 
    if its closed and the Degree."""
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
"""degree = 3
cvs = [(i,ii,0) for i in range(2) for ii in range(2)]
#[(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0)]
cvs.append(cvs[0])
cvs.append(cvs[1])
cvs.append(cvs[2])
#[(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (0, 0, 0), (0, 1, 0), (1, 0, 0)]
knots = _getKnots(count = len(cvs), closed = True, degree = degree)
 
cmds.curve( point = cvs, knot = knots, per = True, degree = degree )"""