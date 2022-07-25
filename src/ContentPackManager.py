from src.OptionsGUI import OptionsGUI
from panda3d.core import VirtualFileSystem, Filename, getModelPath, GraphicsStateGuardian
import glob
from .PropGUI import PropGUI

class ContentPackManager(OptionsGUI):
    '''Generates a content pack manager with GUI to set the GUI for a restart'''
    def __init__(self) -> object:
        super().__init__()


# class ContentPackGUI(OptionsGUI):
    # self.accept('')

