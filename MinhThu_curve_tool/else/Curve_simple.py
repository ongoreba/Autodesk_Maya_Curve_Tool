from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import PySide2 as QT
import maya.cmds as cmds

from . import curve

##########################################################################################################################
#Loggers are nice way to Log Messages/Errors/Warnings to the UI...
import logging
log = logging.getLogger( 'MyTool' )

# HERE is a good (but slightly out of date) Help page for PySide API
# https://www.riverbankcomputing.com/static/Docs/PyQt4/classes.html





##########################################################################################################################
class Thu_window (MayaQWidgetDockableMixin, QT.QtWidgets.QMainWindow):
	"""Simple UI Example for Maya.
	MayaQWidgetDockableMixin >> Inherits the Maya Dockable Functionality.
								This does all the Maya C++ Wrapping to ensure Pyside can properly talk with Maya.
	QMainWindow	>>				Inherits the PySide Main Window Functionality."""

	def __init__(self, parent = None):
		"""Initializes the new Window Tool."""
		super(Thu_window, self).__init__(parent = parent)

		self.setWindowTitle("My Fancy Tool 1.2")
		#Set the CENTRAL/MAIN widget for the UI...
		self.wdgMain =		QT.QtWidgets.QWidget(self)
		self.setCentralWidget(self.wdgMain)
		
		#-----------------------------------------
		# MAKE FIRST TAB WIDGET...nb
		#    -It will be a Scrollable widget
		#-----------------------------------------
		#Create a Text Input Widget for the UI...
		#  https://www.riverbankcomputing.com/static/Docs/PyQt4/qlineedit.html
		self.txtInput = QT.QtWidgets.QLineEdit( self )   			#LINE EDIT is a Text field that you can input text
		self.txtInput.setToolTip ('Input Text for manipulation')	#We are adding a tool tip to this QLineEdit Widget (self.txtInput )
		self.txtInput.setText('Example')							#HERE we are setting the TEXT
		self.txtInput.editingFinished.connect( self.updateUI )		#Refresh the UI to reflect changes to the Text Input

		#Create a update Label
		self.lblUpdate = QT.QtWidgets.QLabel( self )

		
		
		#-----------------------------------------
		#Create a Button that will Execute a Script
		#-----------------------------------------
		self.btnDo = QT.QtWidgets.QPushButton('Curve', self.wdgMain )
		self.btnDo.setToolTip('Make a curve Ctrl')
		self.btnDo.released.connect(self.doTool)					#Connect to the script execution when the button is pressed
		
		#-----------------------------------------
		#Layout the widgets ....
		# -First layout the Label and TextInput horizontally...
		# -Secondly, layout the tool input and the button vertical... with a vertical space between the input and button
		layInput = QT.QtWidgets.QHBoxLayout( )	#No Parent means floating layout... this layout will be added into another one
		layInput.addWidget (self.lblUpdate )
		layInput.addWidget (self.txtInput )
		

		layMain = QT.QtWidgets.QVBoxLayout(self.wdgMain )	# This layout will be placed in the main widget
		layMain.addLayout(layInput)
		layMain.addStretch()
		layMain.addWidget(self.btnDo)

		#Refresh The UI when it is first created...
		self.updateUI()
		
		
	def updateUI( self ):
		"""Will update the UI to keep the relevant Widgets in sycn...
		ie.   The Label should reflect what the TextInput is set to."""
		self.lblUpdate.setText ( 'Update... <{0}>'.format(self.txtInput.text() ) ) 

	def doTool( self ):
		"""Executes the Tool.
		This should print out the Text in the Input Screen."""
		log.info( "Checking... {0}".format(self.txtInput.text() ) )
		curve.create ( name = "curve" , preset = "square" , size = 1 , parent = None , color = None )


##########################################################################################################################
def launchUI():
	#Here we are trying to find if the WINDOW has already been made
	#If it already exists, we just want to push it to the front of all the windows (it might be hidden)
	#By Default, we are going to STORE the window in a GLOBAL variable called 'my_tool'
	window = None
	uiName = 'my_tool'
	
	#This condition is checking to see if 'my_tool' is in the GLOBAL variables...
	#    AND if it is in the Global Variables... is it visible
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
	#So we make a brand new Thu_window window
	nuWindow = Thu_window()
	#Here we are storing the Window in the Global Variables
	# globals()   is a function that returns a dictionary or all the global variables
	# globals()[uiName]  = nuWindow    stores the new window in the global variables 
	globals()[uiName] = nuWindow
	
	#Here we are SHOWING the Window
	#    This function is part of the MayaQWidgetDockableMixin part of our new window
	#    dockable = True    means we can DOCK the window in the Maya UI
	#    floating = True    means that by default it is not docked, and floating in the UI
	nuWindow.show (dockable = True, floating = True)
	return window
	





