## Overview
This script will create curves with custom names as you wish. It also has a really cute pink UI option if you want something 💕 extra 💕
<p align="center">
  <img src="https://cdnb.artstation.com/p/assets/covers/images/075/006/761/smaller_square/thu-nguyen-thu-nguyen-pinktool.jpg?1713493970" />
</p>

## Usage
- Copy the folder MinhThu_curve_tool to this directory: C:\Users\YourName\OneDrive\Documents\maya\scripts
- Open file Curve_Tool_Launch.py in maya script editor and run it.
## General notes
- The size of the curve can't be changed.
- *arrow_circle* and *triangle* options are broken, I'm working on it.
- It's dockable.
## Release notes
Mar. 31, 2025: Fixed the issue of PySide importing in Maya 2025.
## Troubleshooting
- If there is any issues with PySide importing in previous versions of Maya, go to MinhThu_curve_tool/ui/dialogs/curve_maker_dialog. In line 2 you should see
```
import PySide6 as QT
```
change it into
```
import PySide2 as QT
```
If it's still not working please feel free to let me know!
## Acknowledgement
[Charlie McKenna](linkedin.com/in/charlie-mckenna-0b43851) and [Mitch Deeming](linkedin.com/in/mitchelldeeming) are the people that helps reviewing and making the code better. Check them out!
