# Anything that IS NOT color goes in here.
BASE_STYLESHEET = """
QWidget{
	font: 11pt "Tahoma";
    padding: 5px;
}

QToolButton{
    size: 60px 20px;
    border-radius: 10px;
    margin: 8px 1px;
}

QLineEdit{    
    min-height: 20px;
    max-height: 30px;
    border-radius: 10px;
    padding: 10px;
	border: 2px;
    margin: 8px 1px;
}
QPushButton{    
    min-height: 20px;
    max-height: 25px;
    border-radius: 10px;
    padding: 5px;
	border: 2px;
}
"""
# Anything that IS color for the
# dark stylesheet goes in here.
DARK_STYLESHEET = BASE_STYLESHEET + """

QWidget {
    background: #400d1c;
}

QToolButton{
    color: white;
}
QToolButton:checked {
    background-color: #602040;
    border: none;
}

QToolButton::hover:!pressed {
    background-color: #2a0913;
    border: none;
}

QLabel {
    color: white;
}

QLineEdit {
    background: #72404f;
    color: white;
    border: solid #262626;
}

QPushButton {
    color: white;
    background:#72404f;
}

QPushButton::pressed {
    background-color: #af4b69;
    border: none;
}

QPushButton#toggle {
    color: #ffff99;
}

QPushButton::hover:!pressed {
   background-color: #805360;
   border: none;
}
"""
# Anything that IS color for the
# light stylesheet goes in here.
LIGHT_STYLESHEET = BASE_STYLESHEET + """

QWidget{
    background: #ffe6ff;
}

QLabel{
    color: #894358;
}

QLineEdit {
    color: #4d0026;
    background: #e9c4d9;
}

QToolButton{
    color: #894358;
}

QToolButton:checked {
    background-color: #eac7db;
    border: none;
}

QToolButton::hover:!pressed {
    background-color: #e8b5c8;
    border: none;
}

QPushButton {
    color: #894358;
    background: #e9c4d9;
}

QPushButton::pressed {
    background-color: #d194a6;
    border: none;
}

QPushButton#toggle {
    color: #6c82ac;
}

QPushButton::hover:!pressed {
   background-color: #d1b0c3;
   border: none;
}
"""