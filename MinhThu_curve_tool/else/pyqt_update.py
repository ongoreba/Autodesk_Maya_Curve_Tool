import os
import logging
import PySide2 as QT
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from . import curve_maker_tool
ICON_DIRECTION = os.path.join(os.path.dirname(__file__), 'icons')
LOG = logging.getLogger('Curve Tool')
CSS = """
QWidget{	
	background-color: rgb(234,204,244);
	color: rgb(159, 80, 115);
	font: 10pt "Times New Roman";
}
QPushButton{
	background-color: rgba( 255, 228, 4 , 250);
	border: 600px;
	min-height: 40px;
	color: rgb(111, 56, 141);
	font: bold 15pt;
}
"""
class ToolWindow(MayaQWidgetDockableMixin, QT.QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(ToolWindow, self).__init__(parent=parent)
		# How big is the Icon
		iconSize = 60
		# Set how many numbers of rows we want in the grid
		maxNumOfIconsInRow = 5
		# Set the name of the window
		self.setWindowTitle("Curve Tool")
		# Set the main window to put the buttins in
		self.mainWidget = QT.QtWidgets.QWidget(self)
		self.setCentralWidget(self.mainWidget)
		
		# Create a grid of buttons for the curve
		# When we make a grid, PyQt will start placing it from 
		# the top left -> right, from x -> y, start from 0.
		# It looksike this:
		# |  0  |  1  |  2  |
		layButtons = QT.QtWidgets.QGridLayout( )
		# Set the buttons into a group
		self.btnGroupPresets = QT.QtWidgets.QButtonGroup(self)
		# Set the default number of column in the grid
		col = 0
		# Set the default number of row in the grid
		row = 0
		for iconData in [
			(curve_maker_tool.PRESET_SQUARE, 'squareImage.png'), 
			(curve_maker_tool.PRESET_CUBE, 'cubeImage.png'), 
			(curve_maker_tool.PRESET_CIRCLE, 'circleImage.png')
			]:
			iconPreset, iconImage = iconData

			btnIcon = QT.QtWidgets.QToolButton(self.mainWidget)
			btnIcon.setText(iconPreset)
			btnIcon.setIconSize(QT.QtCore.QSize(iconSize, iconSize))
			icon = QT.QtGui.QIcon(os.path.join(ICON_DIRECTION, iconImage))
			btnIcon.setIcon(icon)
			btnIcon.setToolButtonStyle(QT.QtCore.Qt.ToolButtonTextUnderIcon)
			# Set the button to be checkable
			btnIcon.setCheckable (True)
			self.btnGroupPresets.addButton(btnIcon)
			# Add the column for the button, starting from the 1st row 
			# (QWidget, int row, int column,
			#  int rowSpan, int columnSpan)
			layButtons.addWidget(btnIcon, row, col, 1, 1)
			col += 1
			# If the number of column reach the max number
			if col == maxNumOfIconsInRow:
				col = 0  # Reset the column to 0
				row += 1
		'''layButtons = QT.QtWidgets.QGridLayout( )
		# Set the buttons into a group
		self.btnNamePresets  = QT.QtWidgets.QButtonGroup( self )
		# Set the default number of column in the grid
		
		colName = 0
		rowName = 0
		for name in 	[ ('prefix'),
					 	('name'),
					   	('suffix')]:
			buttonName = name

			btnName = QT.QtWidgets.QToolButton ( self.mainWidget  )
			btnName.setText(buttonName)

			self.btnNamePresets.addButton( btnName )
			# Add the column for the button, starting from the 1st row ( QWidget, int row, int column , 
			#                                                           int rowSpan, int columnSpan)
			nameButtons.addWidget( btnName, rowName, colName, 1, 1 )
			#if self.btnNamePresets [0]:
				#print ("onee")
			colName += 1
			if colName == maxNumOfNameInRow:		# if the number of column reach the max number
				colName = 0			# Reset the column to 
				rowName += 1'''
		# self.cmbIcon = QT.QtWidgets.QComboBox( self.mainWidget ) 
		# self.cmbIcon.addItem( 'square' )
		# self.cmbIcon.addItem( 'cube' )
		# self.cmbIcon.addItem( 'circle' )
		
		self.createCtrlBtn = QT.QtWidgets.QPushButton("CREATE CONTROL", self.mainWidget)
		self.createCtrlBtn.released.connect(self.createControl)

		# QLineEdit is a Text field that you can input text
		self.prefixInput = QT.QtWidgets.QLineEdit(self) 
		# Add a tool tip to this Widget			
		self.prefixInput.setToolTip('Set the prefix of the curve')
		# Add a placeholder text so user will know what to input
		self.prefixInput.setPlaceholderText('Curve prefix')
		# Connect the input prefix into the "Current curve name" label
		self.prefixInput.textChanged.connect(self.updateUI)

		# QLineEdit is a Text field that you can input text
		self.nameInput = QT.QtWidgets.QLineEdit(self) 
		# Add a tool tip to this Widget		
		self.nameInput.setToolTip('Set the name of the curve')
		# Add a placeholder text so user will know what to input
		self.nameInput.setPlaceholderText('Curve name')
		# Connect the input name into the "Current curve name" label
		self.nameInput.textChanged.connect(self.updateUI)

		# QLineEdit is a Text field that you can input text
		self.suffixInput = QT.QtWidgets.QLineEdit(self) 
		# Add a tool tip to this Widget			
		self.suffixInput.setToolTip('Set the suffix of the curve')
		# Add a placeholder text so user will know what to input
		self.suffixInput.setPlaceholderText('Curve suffix')
		# Connect the input suffix into the "Current curve name" label
		self.suffixInput.textChanged.connect(self.updateUI)
		
		self.lblUpdate = QT.QtWidgets.QLabel(self)
		# No Parent means floating layout... this layout will be added into another one
		layInput = QT.QtWidgets.QHBoxLayout()  
		layInput.addWidget(self.prefixInput)
		layInput.addWidget(self.nameInput)
		layInput.addWidget(self.suffixInput)
		
		layUpdate = QT.QtWidgets.QHBoxLayout()
		layUpdate.addStretch()
		layUpdate.addWidget(self.lblUpdate)
		layUpdate.addStretch()
		
		layMain = QT.QtWidgets.QVBoxLayout(self.mainWidget)
		layMain.addLayout(layButtons)
		layMain.addLayout(layUpdate)
		layMain.addLayout(layInput)
		#layMain.addLayout(nameButtons)
		layMain.addStretch()
		layMain.addWidget(self.createCtrlBtn)
		# Run the CSS Style sheet
		self.setStyleSheet(CSS)

	# Refresh The UI when it is first created
	def updateUI(self):
		"""Will update the UI to keep the relevant Widgets in sycn...
		ie.   The Label should reflect what the TextInput is set to."""
		text = self.getCurrentName()  #.lower() if you want to turn everything into lowercase
		self.lblUpdate.setText('Current curve name: {0}'.format(text)) 
	
	def getCurrentName(self):
		"""Will get the current name of the curve"""
		currentName = "{0}{1}{2}".format(
			self.prefixInput.text(), 
			self.nameInput.text(),  # .capitalize() if you want to capitalize all
			self.suffixInput.text() 
			)
		return currentName
	
	def getIconPreset(self):
		checkedBtn = self.btnGroupPresets.checkedButton()
		if checkedBtn is None:
			iconPreset = ""
		else:
			iconPreset = checkedBtn.text()
		return iconPreset

	def createControl(self):	
		# Finding which button on the list is selected
		currentIconPreset = self.getIconPreset()
		if currentIconPreset == "":
			LOG.warning("Please select an icon")
			return
		controlName = self.getCurrentName()
		if controlName == "":
			controlName = currentIconPreset
		# Hook up the curve name with the updating button
		LOG.info("Create the Control: {0}".format(currentIconPreset))
		curve_maker_tool.createCurveCtrl(name=controlName, preset=currentIconPreset)



def launchUI():
	#Here we are trying to find if the WINDOW has already been made
	#If it already exists, we just want to push it to the front of all the windows (it might be hidden)
	#By Default, we are going to STORE the window in a GLOBAL variable called 'my_tool'
	window = None
	uiName = 'my_tool'
	
	#This condition is checking to see if 'my_tool' is in the GLOBAL variables...
	#	AND if it is in the Global Variables... is it visible
	#  This is how we can tell if the Window already exists...
	if uiName in globals() and globals()[uiName].isVisible():
		#Here we are getting the WINDOW (We dont have to make a new one)
		window = globals()[uiName]
		if window.isVisible():
			#Here we are making sure it is SHOWN
			window.show()
			#Here we are RAISING it to the top (infront) of all the other windows
			window.raise_()
			#All done, exit the function and don't do anything else
			return None


	#If we get this far, we know the Window has not been made...
	#So we make a brand new ToolWindow window
	nuWindow = ToolWindow()
	#Here we are storing the Window in the Global Variables
	# globals()   is a function that returns a dictionary or all the global variables
	# globals()[uiName]  = nuWindow	stores the new window in the global variables 
	globals()[uiName] = nuWindow
	
	#Here we are SHOWING the Window
	#	This function is part of the MayaQWidgetDockableMixin part of our new window
	#	dockable = True	means we can DOCK the window in the Maya UI
	#	floating = True	means that by default it is not docked, and floating in the UI
	nuWindow.show(dockable=True, floating=True)
	return window





