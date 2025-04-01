import logging

from .dialogs.curve_maker_dialog import CurveMakerDialog
from .dialogs.css_stylesheet import LIGHT_STYLESHEET, DARK_STYLESHEET
from MinhThu_curve_tool.core import curve_maker_tool
from MinhThu_curve_tool.core import curve_presets

LOG = logging.getLogger('Curve Tool')

class CurveMakerController(object):
    def __init__(self, parent=None):
        """ Connect the UI's dialogs and the business logic.
        __init__ will contains all the main layouts of the
        UI and all its main functions
        """
        # Define the UI from the dialog
        self.ui = CurveMakerDialog()
        # Connects all the widgets
        self._initConnections()
        # Connect the presets in the QToolButton to the UI
        self._initPresetButtons()
        # Turn off the dark mode
        self.dark_mode_enabled = False
        self.toggle_dark_mode()
        # Set the stylesheet for the UI
        self.ui.setStyleSheet(DARK_STYLESHEET)


    def _initConnections(self):
        """Connects the widgets in the dialog to the business logic"""
        # Connect the create button into the create control function
        self.ui.createCtrlBtn.released.connect(self.createControl)
        # Connect the input prefix into the "Current curve name" label
        self.ui.prefixInput.textChanged.connect(self.updateUI)
        # Connect the input name into the "Current curve name" label
        self.ui.nameInput.textChanged.connect(self.updateUI)
        # Connect the input suffix into the "Current curve name" label
        self.ui.suffixInput.textChanged.connect(self.updateUI)
        # Connect the make UI button the the UI changing function
        self.ui.makeUIBtn.released.connect(self.toggle_dark_mode)

    def _initPresetButtons(self):
        """A loop to store all the curve buttons' information"""
        # Using a loop to create the buttons in the grid
        # For each of the button's preset:
        for iconData in [
            (curve_maker_tool.PRESET_SQUARE, 'squareImage.png'), 
            (curve_maker_tool.PRESET_CUBE, 'cubeImage.png'), 
            (curve_maker_tool.PRESET_CIRCLE, 'circleImage.png'),
            (curve_maker_tool.PRESET_COG, 'cogImage.png'), 
            (curve_maker_tool.PRESET_ARROW, 'arrowImage.png'), 
            (curve_maker_tool.PRESET_ARROW_CUBE, 'arrowcubeImage.png'),
            (curve_maker_tool.PRESET_ARROW_CIRCLE, 'arrowcircleImage.png'),
            (curve_maker_tool.PRESET_TRIANGLE, 'triangleImage.png')
            ]:
            # Add them into the preset button in the dialog
            self.ui.addPresetButton(iconData[0], iconData[1])

    def updateUI(self):
        """Will update the UI to keep the relevant Widgets in sycn...
        ie. The Label should reflect what the TextInput is set to."""
        text = self.getCurrentName()  #.lower() for lowercase

        self.ui.lblUpdate.setText('Current curve name: {0}'.format(text))

    def getCurrentName(self):
        """Will get the current name of the curve"""
        # Just a simple formatting for the name
        currentName = "{0}{1}{2}".format(
            self.ui.prefixInput.text(), 
            self.ui.nameInput.text(),
            self.ui.suffixInput.text() 
            )
        # Spit out current curve name
        return currentName
    
    def getIconPreset(self):
        """ Will get the name of the curve's button for you
        """
        checkedBtn = self.ui.btnGroupPresets.checkedButton()
        # If there isn't any checked button:
        if checkedBtn is None:
            # Spits out nothing for the preset
            iconPreset = ""
        # If there is any checked button:
        else:
            # Spits out the preset name of the button
            iconPreset = checkedBtn.text()
        return iconPreset
    
    def createControl(self):	
        """Create the control for the curve buttons"""
        # Finding if there's any checked button
        currentIconPreset = self.getIconPreset()
        # If there is no selected icon
        if currentIconPreset == "":
            # Then display a warning
            LOG.warning("Please select an icon")
            # Return to nothing
            return
        # If something is selected
        # then get the control name
        controlName = self.getCurrentName()
        # If the name is nothing,
        if controlName == "":
            controlName = currentIconPreset
        # Show the newly made curve's name to confirm
        LOG.info(
            "Create the Control: {0}".format(currentIconPreset)
            )
        curve_maker_tool.createCurveCtrl(
            name=controlName, 
            preset=currentIconPreset,
            size = 1)
    
    def toggle_dark_mode(self):
        """Switch between dark mode and light mode"""
        self.dark_mode_enabled = not self.dark_mode_enabled
        if self.dark_mode_enabled:
            # set stylesheet to dark mode
            self.ui.setStyleSheet(DARK_STYLESHEET)
            # Set the button's text
            self.ui.makeUIBtn.setText('Light ☀')
        else:
            # set stylesheet to light mode
            self.ui.setStyleSheet(LIGHT_STYLESHEET)
            # Set the button's text
            self.ui.makeUIBtn.setText('Dark ◯')

    
    def show(self, dockable=True, floating=True):
        """Show the UI window
        Args:
            dockable (bool): Window's dockability
                Default: True
            floating (bool): Is the window floating around?
                Default: True
        Returns: 
            A window with UI elements and working tools
        """
        #launchUI()
        self.ui.show(dockable=dockable, floating=floating)

    def isVisible(self):
        """Controls the window's visibility
        Returns:
        A visible window"""
        return self.ui.isVisible()

def launchUI():
    #Here we are trying to find if the WINDOW has already been made
    #If it already exists, we just want to push it to the front of 
    #all the windows (it might be hidden)
    #By Default, we are going to STORE the window in a 
    #GLOBAL variable called 'my_tool'
    window = None
    uiName = 'Minh_Thu_Tool_<3'
    #This condition is checking to see if 'my_tool' 
    #is in the GLOBAL variables...
    #	AND if it is in the Global Variables... is it visible
    #  This is how we can tell if the Window already exists...
    if uiName in globals() and globals()[uiName].isVisible():
        #Here we are getting the WINDOW (We dont have to make a new one)
        window = globals()[uiName]
        if window.isVisible():
            #Here we are making sure it is SHOWN
            window.show()
            #Here we are RAISING it to the top (infront) 
            #of all the other windows
            window.raise_()
            #All done, exit the function and don't do anything else
            return None

    #If we get this far, we know the Window has not been made...
    #So we make a brand new CurveMakerDialog window
    nuWindow = CurveMakerController()
    #Here we are storing the Window in the Global Variables
    # globals()   is a function that returns a 
    # dictionary or all the global variables
    # globals()[uiName]  = nuWindow	stores the new
    # window in the global variables 
    globals()[uiName] = nuWindow
    
    # Here we are SHOWING the Window
    # This function is part of the MayaQWidgetDockableMixin 
    # part of our new window
    #	dockable = True	means we can DOCK the window in the Maya UI
    #	floating = True	means that by default it is not docked, 
    #   and floating in the UI
    nuWindow.show(dockable=True, floating=True)
    return window
