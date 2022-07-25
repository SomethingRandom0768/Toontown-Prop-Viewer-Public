# Imports

# # Panda3D imports 
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile


# GUI Imports
from src.PropGUI import *
from src.PlaygroundManager import PlaygroundManager
from src.OptionsManager import OptionsManager

# MISC Imports
import sys

loadPrcFile("config/Config.prc")

class ToontownPropViewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        options = OptionsManager()
        playgroundManager = PlaygroundManager()
        propGUIManager = PropGUI('phase_3/models/char')
        self.accept('escape', sys.exit)
    
app = ToontownPropViewer()
app.run()