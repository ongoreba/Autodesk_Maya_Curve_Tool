    """Create a New Curve Ctrl

    Args:
      name (str): The name of the base new curve to be created. 
          Default: curve
      preset (str): The type of curve to create.
          Default: square
          Valid values: circle, square, 
      size (int): Factor to scale the created curve by.
          Default: 1
      parent (str|None): Name of the object to parent the curve too.
          Default: None
      color (list|None): A list containing 3 floats for RGB values or None.
          Default: None

    Returns:
      str: The name of the newly created curve.
  """


    """Interactive curve creating tool
    Args:
    selectedObjects (list|str): List of Nodes to create a curve for.
        Default: None
    suffix="Ctrl", 
    preset="square"

               <bool>    if True, create a  curve for everything selected in the scene """
     
