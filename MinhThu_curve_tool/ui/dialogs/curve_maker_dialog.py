import os
import PySide6 as QT
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# Set the direction where we will retrieve the icon data
ICON_DIRECTION = os.path.join(
    os.path.dirname(
        os.path.dirname(__file__)), 
        'icons'
)

class CurveMakerDialog(MayaQWidgetDockableMixin, QT.QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CurveMakerDialog, self).__init__(parent=parent)
        """ Make the UI for the curve_maker_tool
        __init__ contains all the PyQt stuffs and layout
        """
        # How big is the width of the mainWidget
        w = 500
        # How big is the height of the mainWidget
        h = 300

        # Set the icon size
        self.iconSize = 60
        # Set how many numbers of rows we want in the grid
        self.maxNumOfIconsInRow = 5

        # Set the name of the window
        self.setWindowTitle("Curve Tool")
        # Set the main window to put the buttons in
        self.mainWidget = QT.QtWidgets.QWidget(self)
        # Make it a central widget
        self.setCentralWidget(self.mainWidget) 
        # resize main window
        self.resize(w, h)

        # Create a grid of buttons for the curve
        # When we make a grid, PyQt will start placing it from
        # the top left -> right, from x -> y, start from 0.
        # It looksike this:
        # |  0  |  1  |  2  |
        self.layButtons = QT.QtWidgets.QGridLayout( )
        # Set the buttons into a group
        self.btnGroupPresets = QT.QtWidgets.QButtonGroup(self)
        
        # Create a layout for label updator
        self.lblUpdate = QT.QtWidgets.QLabel(self)

        # QLineEdit is a Text field that you can input text
        # Create the widget to change the name
        self.prefixInput = QT.QtWidgets.QLineEdit(self) 
        # Add a tool tip to this Widget			
        self.prefixInput.setToolTip('Set the prefix of the curve')
        # Add a placeholder text so user will know what to input
        self.prefixInput.setPlaceholderText('Curve prefix')

        # Create the widget to change the name
        self.nameInput = QT.QtWidgets.QLineEdit(self) 
        # Add a tool tip to this Widget		
        self.nameInput.setToolTip('Set the name of the curve')
        # Add a placeholder text so user will know what to input
        self.nameInput.setPlaceholderText('Curve name')

        # Create the widget to change the suffix
        self.suffixInput = QT.QtWidgets.QLineEdit(self) 
        # Add a tool tip to this Widget			
        self.suffixInput.setToolTip('Set the suffix of the curve')
        # Add a placeholder text so user will know what to input
        self.suffixInput.setPlaceholderText('Curve suffix')
        
        # Create the Push button to make the control
        self.createCtrlBtn = QT.QtWidgets.QPushButton(
            "CREATE CONTROL", self.mainWidget
            )
        
        # Create the Push button to change the UI
        self.makeUIBtn = QT.QtWidgets.QPushButton(
            "CHANGE UI", self.mainWidget
            )
        # Set the name of the widget so we know which one is 
        # the UI changing buttton in the CSS Style Sheet
        self.makeUIBtn.setObjectName('toggle')
        
        # Create a floating layout for the updating label
        self.layUpdate = QT.QtWidgets.QHBoxLayout()
        # Add streth so user can stretch the UI
        self.layUpdate.addStretch()
        # Add the label update widget here
        self.layUpdate.addWidget(self.lblUpdate)
        self.layUpdate.addStretch()

        # Create a floating horizontal layout for name input
        self.layInput = QT.QtWidgets.QHBoxLayout()
        # Add all the naming-related widgets in here
        self.layInput.addWidget(self.prefixInput)
        self.layInput.addWidget(self.nameInput)
        self.layInput.addWidget(self.suffixInput)
      
        # Put the layouts we did ealier into place
        layMain = QT.QtWidgets.QVBoxLayout(self.mainWidget)
        # Add the curves' buttons
        layMain.addLayout(self.layButtons)
        layMain.addStretch()
        # Add the label update widget
        layMain.addLayout(self.layUpdate)
        # Add the name input widget
        layMain.addLayout(self.layInput)
        layMain.addStretch()
        # Add the "create button" button
        layMain.addWidget(self.createCtrlBtn)
        # Add the UI changing button
        layMain.addWidget(self.makeUIBtn)

        # This is a cat
        #  ^--^---
        # ('w'     )=== MEOW
        #  v-----vv

    def addPresetButton(self, preset, iconImage):
        """ Create the buttons with curve icons
        Args:
            preset(str): The preset of the curve
            iconImage(file path): The button's icon image
        """
        # Set the direction for the button's icon
        # it's a combination between 
        # the global attr ICON_DIRECTION and 
        # the local attr iconImage that we defined earlier
        icon = QT.QtGui.QIcon(os.path.join(ICON_DIRECTION, iconImage))
        # QToolButton is the button that allows us to make
        # real cute and big icons ^W^
        btnIcon = QT.QtWidgets.QToolButton(self.mainWidget)
        # Set the default text for the button
        # It's the string of name retrieved from preset
        btnIcon.setText(preset)
        # Set the size of the button's icon
        btnIcon.setIconSize(QT.QtCore.QSize(self.iconSize, self.iconSize))
        # Set the icon image for the button
        btnIcon.setIcon(icon)
        # Set the text position for the button, 
        # in this case under the icon
        btnIcon.setToolButtonStyle(QT.QtCore.Qt.ToolButtonTextUnderIcon)
        # Set the button to be checkable so if
        # we check it, we can't check another button
        btnIcon.setCheckable (True)

        # Calculate the row and column from the total number of buttons
        row = len(self.btnGroupPresets.buttons()) // self.maxNumOfIconsInRow
        col = len(self.btnGroupPresets.buttons()) % self.maxNumOfIconsInRow

        # Add the newly made button into the group
        self.btnGroupPresets.addButton(btnIcon)
        # Add the column for the button, starting from the 1st row 
        # (QWidget, int row, int column,
        # int rowSpan, int columnSpan)
        self.layButtons.addWidget(btnIcon, row, col, 1, 1)


