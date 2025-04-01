from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import PySide2 as QT
import maya.cmds as cmds

##########################################################################################################################
#Loggers are nice way to Log Messages/Errors/Warnings to the UI...
import logging
log = logging.getLogger( 'MyTool' )

# HERE is a good (but slightly out of date) Help page for PySide API
# https://www.riverbankcomputing.com/static/Docs/PyQt4/classes.html





##########################################################################################################################
class window_tool (MayaQWidgetDockableMixin, QT.QtWidgets.QMainWindow):
	"""Simple UI Example for Maya.
	MayaQWidgetDockableMixin >> Inherits the Maya Dockable Functionality.
								This does all the Maya C++ Wrapping to ensure Pyside can properly talk with Maya.
	QMainWindow	>>				Inherits the PySide Main Window Functionality."""

	def __init__(self, parent = None):
		"""Initializes the new Window Tool."""
		super(window_tool, self).__init__(parent = parent)

		self.setWindowTitle("My Fancy Tool 1.2")
		
		
		
		#Set the CENTRAL/MAIN widget for the UI...
		self.tabWidget = 	QT.QtWidgets.QTabWidget(self)
		self.setCentralWidget(self.tabWidget)
		# self.mainWidget = QT.QtWidgets.QWidget(self )
		# self.setCentralWidget(self.mainWidget)
		
		#-----------------------------------------
		# MAKE FIRST TAB WIDGET...
		#    -It will be a Scrollable widget
		#-----------------------------------------
		self.scrollFirst = QT.QtWidgets.QScrollArea (self )
		self.tabWidget.addTab( self.scrollFirst, "First" )
		
		self.wdgMain = QT.QtWidgets.QWidget(self.scrollFirst)
		self.scrollFirst.setWidget (self.wdgMain )
		self.scrollFirst.setWidgetResizable(1)
		#Create a Text Input Widget for the UI...
		#  https://www.riverbankcomputing.com/static/Docs/PyQt4/qlineedit.html
		self.txtInput = QT.QtWidgets.QLineEdit( self.wdgMain )   	#LINE EDIT is a Text field that you can input text
		self.txtInput.setToolTip ('Input Text for manipulation')	#We are adding a tool tip to this QLineEdit Widget (self.txtInput )
		self.txtInput.setText('Example')							#HERE we are setting the TEXT
		self.txtInput.editingFinished.connect( self.updateUI )		#Refresh the UI to reflect changes to the Text Input

		#Create a update Label
		self.lblUpdate = QT.QtWidgets.QLabel( self.wdgMain )

		
		
		#-----------------------------------------
		#LETS CREATE a GROUP BOX and put a widget inside of it
		#-----------------------------------------
		self.grpOptions = QT.QtWidgets.QGroupBox( 'Options', self.wdgMain )
		
		self.chkOptionA = QT.QtWidgets.QCheckBox( 'OptionA', self.grpOptions )
		self.chkOptionB = QT.QtWidgets.QCheckBox( 'OptionB', self.grpOptions )
		self.chkOptionC = QT.QtWidgets.QCheckBox( 'OptionC', self.grpOptions )
		
		layChecks = QT.QtWidgets.QHBoxLayout(  )
		#layOptions.setContentsMargins( 0, 0, 0, 0 )
		layChecks.setSpacing ( 20 )
		layChecks.addWidget(self.chkOptionC)
		layChecks.addWidget(self.chkOptionB)
		layChecks.addWidget(self.chkOptionA)
		layChecks.addStretch ( )
		
		self.radOptionA = QT.QtWidgets.QRadioButton( 'RadioA', self.grpOptions )
		self.radOptionB = QT.QtWidgets.QRadioButton( 'RadioB', self.grpOptions )
		self.radOptionC = QT.QtWidgets.QRadioButton( 'RadioC', self.grpOptions )
		
		self.buttonGroupA = QT.QtWidgets.QButtonGroup( self.grpOptions )
		self.buttonGroupA.addButton (self.radOptionA)
		self.buttonGroupA.addButton (self.radOptionB)
		self.buttonGroupA.addButton (self.radOptionC)
		self.buttonGroupA.buttonToggled.connect ( self.displayRadioGroupA )
		
		
		layRadios = QT.QtWidgets.QHBoxLayout(  )
		#layOptions.setContentsMargins( 0, 0, 0, 0 )
		layRadios.setSpacing ( 20 )
		layRadios.addWidget(self.radOptionA)
		layRadios.addWidget(self.radOptionB)
		layRadios.addWidget(self.radOptionC)
		layRadios.addStretch ( )
		
		
		self.radOptionAA = QT.QtWidgets.QRadioButton( 'RadioAA', self.grpOptions )
		self.radOptionBB = QT.QtWidgets.QRadioButton( 'RadioBB', self.grpOptions )
		self.radOptionCC = QT.QtWidgets.QRadioButton( 'RadioCC', self.grpOptions )
		
		self.buttonGroupB = QT.QtWidgets.QButtonGroup( self.grpOptions )
		self.buttonGroupB.addButton (self.radOptionAA)
		self.buttonGroupB.addButton (self.radOptionBB)
		self.buttonGroupB.addButton (self.radOptionCC)
		
		
		layRadiosB = QT.QtWidgets.QHBoxLayout(  )
		#layOptions.setContentsMargins( 0, 0, 0, 0 )
		layRadiosB.setSpacing ( 20 )
		layRadiosB.addWidget(self.radOptionAA)
		layRadiosB.addWidget(self.radOptionBB)
		layRadiosB.addWidget(self.radOptionCC)
		layRadiosB.addStretch( )
		
		
		
		self.numInteger = QT.QtWidgets.QSpinBox( self.grpOptions )
		self.numInteger.setMaximum ( 1000 )
		self.numInteger.setToolTip ( "This is an Integer Input" )		
		
		self.numFloat = QT.QtWidgets.QDoubleSpinBox( self.grpOptions )
		self.numFloat.setPrefix ( "$" )
		self.numFloat.setRange ( -200, 200 )
		self.numFloat.setSingleStep ( 5 )
		#self.numFloat.valueChanged.connect  ( self.displayCurrentDollarAmount )
		self.numFloat.editingFinished.connect ( self.displayCurrentDollarAmount )
		
		
			
		
		
		layOptions = QT.QtWidgets.QVBoxLayout( self.grpOptions  )
		layOptions.addLayout ( layChecks )
		layOptions.addLayout ( layRadios )
		layOptions.addLayout ( layRadiosB )
		layOptions.addWidget ( self.numInteger )
		layOptions.addWidget ( self.numFloat )
		
		
	
		#-----------------------------------------
		#CREATE a SECOND TAB
		#-----------------------------------------
		self.newTab = QT.QtWidgets.QWidget( self )
		self.tabWidget.addTab( self.newTab, "Make NEW" )
	
	
	
		
		
		#-----------------------------------------
		#Create a Button that will Execute a Script
		#-----------------------------------------
		self.btnDo = QT.QtWidgets.QPushButton('Do', self.wdgMain )
		#icon = QT.QtGui.QIcon ( 'C:/Klei/mayaPipeline/codeBrat/UI/Icons/icon_palette.png' )
		#self.btnDo.setIcon ( icon )
		self.btnDo.setToolTip('Execute the Script')
		self.btnDo.setStatusTip('Execute the Script')
		self.btnDo.released.connect(self.doTool)					#Connect to the script execution when the button is pressed

		#-----------------------------------------
		#ADD a CONTEXT MENU to this button...
		#	-First make a MENU ITEM
		#	-Then Add ACTIONS to the MENU
		#-----------------------------------------
		self.mnuDo =				QT.QtWidgets.QMenu	( 'Do Menu', self )
		
		self.actNew = 				QT.QtWidgets.QAction ( 'New', self )
		self.mnuDo.addAction 		( self.actNew )
		self.actReplace = 			QT.QtWidgets.QAction ( 'Replace', self )
		self.mnuDo.addAction		( self.actReplace )
		
		#-----------------------------------------
		# SET THE BUTTON to ACCEPT CUSTOM CONTEXT MENU...
		# -Hookup the SIGNAL to go to the SHOW DO MENU function
		#-----------------------------------------
		self.btnDo.setContextMenuPolicy (QT.QtCore.Qt.CustomContextMenu)
		self.btnDo.customContextMenuRequested.connect( self.showDoMenu )
		
		
		
		

		
		#-----------------------------------------
		#Create the CUSTOM COLOR BUTTON
		#-----------------------------------------
		self.btnColor =	QColorButton(self)
		
		#-----------------------------------------
		#Layout the widgets ....
		# -First layout the Label and TextInput horizontally...
		# -Secondly, layout the tool input and the button vertical... with a vertical space between the input and button
		layInput = QT.QtWidgets.QHBoxLayout( )	#No Parent means floating layout... this layout will be added into another one
		layInput.addWidget (self.lblUpdate )
		layInput.addWidget (self.txtInput )
		

		layMain = QT.QtWidgets.QVBoxLayout(self.wdgMain )	# This layout will be placed in the main widget
		layMain.addLayout(layInput)
		layMain.addWidget(self.grpOptions)
		layMain.addStretch()
		layMain.addWidget(self.btnDo)
		layMain.addWidget(self.btnColor)
		
		#Refresh The UI when it is first created...
		self.updateUI()
		
		
	def showDoMenu(self, point ):
		"""This FUNCTION will SHOW the Custom mnuDo whenever a CustomContextMenu is triggered from the btnDo."""
		self.mnuDo.exec_( self.btnDo.mapToGlobal(point) )
		
		
		
	def updateUI( self ):
		"""Will update the UI to keep the relevant Widgets in sycn...
		ie.   The Label should reflect what the TextInput is set to."""
		self.lblUpdate.setText ( 'Update... <{0}>'.format(self.txtInput.text() ) ) 

	def doTool( self ):
		"""Executes the Tool.
		This should print out the Text in the Input Screen."""
		log.info( "Checking... {0}".format(self.txtInput.text() ) )
		
		
	def displayCurrentDollarAmount( self ):
		"""Display the Current Amount in the Float Spin Box."""
		amount = self.numFloat.value ()
		print ("CURRENT AMOUNT " +  str(amount) )
	
	def displayRadioGroupA( self, button, toggled ):
		if toggled == True:
			print ("RADIO GROUP A: " + button.text() )




##########################################################################################################################
class QColorButton(QT.QtWidgets.QPushButton):
	'''Custom Qt Widget to show a chosen color.

	Left-clicking the button shows the color-chooser, while
	right-clicking resets the color to None (no-color).	
	'''

	colorChanged = QT.QtCore.Signal()

	def __init__(self, *args, **kwargs):
		super(QColorButton, self).__init__(*args, **kwargs)

		self._color = None		#STORES the CURRENT COLOR in the WIDGET
		self.setMaximumWidth(32)
		#-----------------------------------------
		# WHEN we press the COLOR BUTTON... we want to start the color picking
		#-----------------------------------------
		self.pressed.connect(self.onColorPicker)

	#================================================================================
	#	COLOR
	#================================================================================
	def getColor(self):
		"RETURNS the color stored in this widget"
		return self._color


	def setColor(self, color):
		"""Sets the Color in this widget"""
		if color != self._color:
			self._color = color
			self.colorChanged.emit()	# WE ARE EMITTING the Color Changed SIGNAL
			
		#-----------------------------------------
		# THIS will update the WIDGET to use the Correct Color
		# 	-Using STYLE SHEETS is an easy way to change how a widget LOOKS without changing how it behaves...
		#-----------------------------------------
		if self._color:
			ss = "QColorButton { background-color: COLOR; border:  none}""".replace("COLOR", self._color.name())
		else: 
			ss = ""
			self.setStyleSheet(ss)


	#================================================================================
	#	COLOR DIALOG
	#================================================================================
	def onColorPicker(self):
		'''Show color-picker dialog to select color.
		Qt will use the native dialog by default.
		'''
		dlg = QT.QtWidgets.QColorDialog(self)
		#-----------------------------------------
		# SET the Current color in the Dialog box to be the stored color (if any)
		#-----------------------------------------
		if self._color:
			dlg.setCurrentColor(QT.QtGui.QColor(self._color))

		#-----------------------------------------
		# Launch the Dialog
		#-----------------------------------------
		if dlg.exec_():
			#-----------------------------------------
			# IF the Dialog is accepted...
			# 	-set the current Color in the widget
			#-----------------------------------------
			self.setColor(dlg.currentColor())
			print ("RED >>", self._color.red())
	#================================================================================
	#	MOUSE EVENTS
	#================================================================================
	def mousePressEvent(self, e):
		#-----------------------------------------
		# CHECK to see if the RIGHT MOUSE BUTTON was clicked on the widget
		#-----------------------------------------
		if e.button() == QT.QtCore.Qt.RightButton:
			#-----------------------------------------
			# IF SO, remove the Current Color from the widget
			#-----------------------------------------
			self.setColor(None)

		return super(QColorButton, self).mousePressEvent(e)



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
	#So we make a brand new window_tool window
	nuWindow = window_tool()
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
	

	
launchUI()




