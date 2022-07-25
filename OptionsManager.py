# SRC imports
from .OptionsGUI import *
from .ContentPackManager import *

# Panda3D imports
from panda3d.core import VirtualFileSystem, Filename, getModelPath, GraphicsStateGuardian, WindowProperties, Multifile
from direct.gui import DirectGui
from direct.gui.DirectGui import *
from direct.interval.LerpInterval import *
from direct.directnotify import DirectNotifyGlobal

# Information processing imports
import glob
import json
import os


class OptionsManager(OptionsGUI):
    notify = DirectNotifyGlobal.directNotify.newCategory("OptionsManager")
    notify.setDebug(1)

    def __init__(self) -> object:
        '''Generates an options manager that the player can change content packs and settings through'''
        super().__init__()

        # Variables
        self.buttonGeom = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_squareButton')
        self.isGUIHidden = True
        vfs = VirtualFileSystem.getGlobalPtr()
        self.__settings = {}
        self.__filename = 'propviewersettings.json'
        self.contentPackButtons = []
        self.currentChosenPack = 0
        self.loadedPacks = []

        # Events
        self.accept('j', self.showOrHideGUI)
        self.accept('t', self.reloadTextures)
        self.accept('wheel_up', self.scrollFrameUp)
        self.accept('wheel_down', self.scrollFrameDown)

        self.generateShowOptionsGUIButton()
        self.generateSettings()
        self.generateOptionsGUI()
        self.notify.debug('Generated')


# GUI FUNCTIONS

    def hideGUI(self):
        self.optionsFrame.hide()
    
    def showGUI(self):
        self.optionsFrame.show()

    def showOrHideGUI(self):
        if self.isGUIHidden:
            self.showGUI()
            self.isGUIHidden = False
            self.showGUIButton['text'] = 'Hide Options\nMenu(J)'
        else:
            self.isGUIHidden = True
            self.showGUIButton['text'] = 'Show Options\nMenu(J)'
            self.hideGUI()

    def generateShowOptionsGUIButton(self):
        self.showGUIButton = DirectButton(
            parent=aspect2d,
            geom=self.buttonGeom,
            relief=None,
            geom_scale=(0.5,0.5,0.75),
            text="Show Options\nMenu(J)",
            text_font=self.modalFont,
            text_scale=0.25,
            scale=0.25,
            pos=(0.5,0,0.9),
            command=self.showOrHideGUI,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )

    def generateOptionsGUI(self):
        optionsFrameGeom = dynamicFrameOnly(25, 30)


        self.optionsFrame = DirectFrame(

            geom=optionsFrameGeom.geom,
            parent=aspect2d,
            pos=(-0.75,0,0.6),
            relief=None
        )
        self.optionsLabel = DirectLabel(
            parent=self.optionsFrame,
            text="Options",
            text_font = self.labelFont,
            text_scale=0.2,
            text_fg=(0, 1, 1, 1),
            pos=(0.75,0,-0.25),
            relief=None
        )

        self.optionsScrollFrame = DirectScrolledFrame(
            frameSize=(0, 1.55, 0,0.95),
            canvasSize=(-1, 1, -5, 1),
            parent=self.optionsFrame,
            pos=(0,0,-1.25),
            verticalScroll_geom = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_lineThick'),
            verticalScroll_thumb_geom = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_slider1'),
            verticalScroll_geom_pos=(1.5,0,0.5),
            verticalScroll_geom_scale=(0.2, 0.25, 0.2),
            verticalScroll_thumb_geom_scale = 0.1,
            verticalScroll_thumb_geom_pos=(-0.01,0,0),
            verticalScroll_incButton_relief=None,
            verticalScroll_decButton_relief=None,
            verticalScroll_geom_hpr=(0,0,90),
            verticalScroll_relief=None,
            verticalScroll_thumb_relief=None,
            horizontalScroll_relief=None,
            relief=None,
            horizontalScroll_frameSize=(0,0,0,0),
            horizontalScroll_thumb_relief=None,
            horizontalScroll_incButton_relief=None,
            horizontalScroll_decButton_relief=None,
            verticalScroll_thumb_rolloverSound=self.guiRolloverSound,
            verticalScroll_thumb_clickSound=self.guiClickSound
        )

        fullscreenToggle = OptionsToggle(self.optionsScrollFrame.getCanvas(), 'Fullscreen:', -0.95, 0.8, self.enableFullscreen, self.disableFullscreen)

        fpsMeterToggle = OptionsToggle(self.optionsScrollFrame.getCanvas(), 'FPS Meter Toggle:', -0.95, 0.65, self.enableFPSMeter, self.disableFPSMeter)

        self.reloadContentPacksButton = DirectButton(
                parent = self.optionsScrollFrame.getCanvas(),
                geom=self.buttonGeom,
                geom_scale=(0.45, 0.4, 0.4),
                scale=0.5,
                text="Reload Packs",
                text_font=self.modalFont,
                text_pos=(0,-0.05,0),
                text_scale=0.1,
                pos=(0.15,0,-0.6),
                relief=None,
                command=self.reloadContentPackOptionsFrame,
                rolloverSound=self.guiRolloverSound,
                clickSound=self.guiClickSound 
        )

        self.removeContentPacksButton = DirectButton(
                parent = self.optionsScrollFrame.getCanvas(),
                geom=self.buttonGeom,
                geom_scale=(0.45, 0.4, 0.4),
                scale=0.5,
                text="Remove Current Pack",
                text_font=self.modalFont,
                text_pos=(0,-0.05,0),
                text_scale=0.1,
                pos=(-0.65,0,-0.6),
                relief=None,
                command=self.removeContentPackPath,
                rolloverSound=self.guiRolloverSound,
                clickSound=self.guiClickSound 
        )

        # self.heightEntry = DirectEntry(
        #     parent=self.optionsScrollFrame.getCanvas(),
        #     pos=(-0.95, 0, 0)
        # )

        # self.widthEntry = DirectEntry(
        #     parent=self.optionsScrollFrame.getCanvas()
        # )
        self.optionsFrame.hide()
        self.generateContentPackFrame()

    def generateContentPackFrame(self):
        contentPackGeom = dynamicFrameOnly(15, 25)
        self.contentPackFrame = DirectFrame(
            geom=contentPackGeom.geom,
            parent=self.optionsScrollFrame.getCanvas(),
            relief=None,
            pos=(-0.925,0, 0.35),

        )

        self.contentPackScrollFrame = DirectScrolledFrame(
            parent=self.contentPackFrame,
            frameSize=(0,1.3,-0.81,0),
            canvasSize=(0,1.3,0,6),
            verticalScroll_geom = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_lineSkinny'),
            verticalScroll_geom_hpr=(0,0,90),
            verticalScroll_thumb_geom = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_slider1'),
            verticalScroll_thumb_geom_scale = 0.075,
            verticalScroll_thumb_geom_pos=(0,0,0),
            verticalScroll_geom_pos=(1.26,0,-0.4),
            verticalScroll_geom_scale=(0.2, 0.25, 0.2),
            verticalScroll_relief=None,
            verticalScroll_thumb_relief=None,
            horizontalScroll_relief=None,
            relief=None,
            horizontalScroll_frameSize=(0,0,0,0),
            horizontalScroll_thumb_relief=None,
            horizontalScroll_incButton_relief=None,
            horizontalScroll_decButton_relief=None,
            verticalScroll_incButton_relief=None,
            verticalScroll_decButton_relief=None,
        )

        self.originalPaths = glob.glob('multifiles/*.mf' )    
        i = 0
        for path in self.originalPaths:
            self.loadedPacks.append(path)
            newerPath = path.replace('multifiles/', '')
            evenNewerPath = newerPath.replace('.mf', '')
            contentPackModal = OptionsModal(self.contentPackScrollFrame.getCanvas(), evenNewerPath, 0, 5.75 - (i * 0.2) )
            contentPackButton = DirectButton(
                parent = self.contentPackScrollFrame.getCanvas(),
                geom=self.buttonGeom,
                geom_scale=0.4,
                scale=0.25,
                text="Select",
                text_pos=(0,-0.05,0),
                text_scale=0.25,
                pos=(1.05, 0, 5.75 - (i * 0.2) ),
                relief=None,
                command=self.updateContentPackPath,
                extraArgs=[path, i],
                rolloverSound=self.guiRolloverSound,
                clickSound=self.guiClickSound 
            )

            self.contentPackButtons.append(contentPackButton)
            i+=1

    def deleteContentPackFrame(self):
        self.contentPackFrame.destroy()

    def deleteOptionsGUI(self):
        self.optionsFrame.destroy()

    def reloadContentPackOptionsFrame(self):
        self.deleteContentPackFrame()
        self.generateContentPackFrame()

    def scrollFrameDown(self):
        self.optionsScrollFrame['verticalScroll_value']+=0.05

    def scrollFrameUp(self):
        self.optionsScrollFrame['verticalScroll_value']-=0.05 

    def resetButtonTexts(self):
        for gui in self.contentPackButtons:
            gui['text'] = 'Select'
        

# SETTINGS RELATED FUNCTIONS
    
    def generateSettings(self):
        if os.path.exists(self.__filename):
            try:
                with open(self.__filename, 'r') as f:
                    self.__settings = json.load(f)
                    self.readSettings()
            except:
                self.__settings = {}

    def readSettings(self):
        if self.__settings['fullscreen'] == False:
            wp = WindowProperties()
            wp.setFullscreen(False)
            base.win.requestProperties(wp)
        else:
            wp = WindowProperties()
            wp.setFullscreen(True)
            base.win.requestProperties(wp)
        
        if self.__settings['fps-meter'] == False:
            base.setFrameRateMeter(False)
        else:
            base.setFrameRateMeter(True)
        
        if self.__settings:
            self.setWindowsSize(self.__settings['resolution'][0], self.__settings['resolution'][1])
        else:
            self.updateSetting('resolution', (640, 480))
            self.writeSettings()
            self.setWindowsSize(640, 480)
        
    def updateSetting(self, setting, value):
        self.__settings[setting] = value

    def getSetting(self, setting, default=None):
        return self.__settings.get(setting, default)

    def writeSettings(self):
        with open(self.__filename, 'w+') as f:
            json.dump(self.__settings, f, indent=4)

# ACTUAL OPTIONS FUNCTIONS

    def enableFullscreen(self):
        wp = WindowProperties()
        wp.setFullscreen(True)
        base.win.requestProperties(wp)
        self.updateSetting('fullscreen', True)
        self.writeSettings()
        self.notify.debug("Fullscreen enabled")
        
    def disableFullscreen(self):
        wp = WindowProperties()
        wp.setFullscreen(False)
        base.win.requestProperties(wp)
        self.updateSetting('fullscreen', False)
        self.writeSettings()
        self.notify.debug("Fullscreen disabled")

    def enableFPSMeter(self):
        base.setFrameRateMeter(True)
        self.updateSetting('fps-meter', True)
        self.writeSettings()  
        self.notify.debug('FPS-meter enabled')

    def disableFPSMeter(self):
        base.setFrameRateMeter(False)
        self.updateSetting('fps-meter', False)
        self.writeSettings()  
        self.notify.debug('FPS-meter disabled')

    def setWindowsSize(self, height, width):
        wp = WindowProperties()
        wp.setSize(width, height)
        base.win.requestProperties(wp)
        self.notify.debug("Resolution is now " + height + " by " + width)

# CONTENT PACK RELATED FUNCTIONS
    def updateContentPackPath(self, contentPackPath, index=None):
        vfs.mount( Filename(contentPackPath), '.', VirtualFileSystem.MFReadOnly)
        self.updateSetting('content-pack', contentPackPath)
        self.writeSettings()
        self.currentChosenPack = index
        self.contentPackButtons[index]['text'] = "Selected"
        self.notify.debug("The current content pack is now " + contentPackPath)
    
    def removeContentPackPath(self):
        vfs.unmount(Filename( self.loadedPacks[self.currentChosenPack] ) )
        self.updateSetting('content-pack', "None")
        self.writeSettings()
        self.resetButtonTexts()
        self.notify.debug("Content Pack removed")

    def reloadTextures(self):
        gsg = base.win.gsg
        gsg.releaseAllTextures()
        self.notify.debug("Reloading Textures")

class OptionsModal(DirectGui.DirectFrame):
    '''This is the left part of any Options Modal, everything else past this class inherits from this and adds to it'''
    notify = DirectNotifyGlobal.directNotify.newCategory('OptionsModal')
    notify.setDebug(1)

    def __init__(self, modalParent, modalText, x, z):
        self.modalFont = loader.loadFont('phase_3/fonts/ImpressBT.ttf')
        self.sliderGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam').find('**/ttr_t_gui_gen_buttons_lineSkinny')
        self.sliderThumbGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam').find('**/ttr_t_gui_gen_buttons_slider2')
        self.selectionFrameThumbGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam').find('**/ttr_t_gui_gen_buttons_slider1')
        self.guiClickSound = loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg')
        self.guiRolloverSound = loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg')
        self.toggleButtonGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam').find('**/ttr_t_gui_gen_buttons_toggleButton')
        self.warmToggleButtonGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam').find('**/*toggleWarm')
        self.coolToggleButtonGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam').find('**/*toggleCool')

        self.containerFrame = DirectGui.DirectLabel(
            parent=modalParent,
            pos=(x, 0, z),
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.01, 0.9, -0.01, 0.06),
            scale=0.9,
        )

        self.modalTextNode = OnscreenText(
            align=TextNode.ALeft,
            text=modalText,
            font=self.modalFont
        )

        self.modalTextNode.reparentTo(self.containerFrame)

class OptionsToggle(OptionsModal):
    '''Creates a toggle that creates an off/on switch'''
    notify = DirectNotifyGlobal.directNotify.newCategory('OptionsToggle')
    notify.setDebug(1)

    def __init__(self, modalParent, modalText, x, z, activateCommand=None, deactivateCommand=None):
        super().__init__(modalParent, modalText, x, z)  # Creates the text on the left

        def executeFunction(self):
            animateToggle()

        self.button = DirectGui.DirectCheckButton(
            scale=0.15,
            relief=None,
            boxImageScale=1,
            boxPlacement=('right'),
            boxImage=(self.warmToggleButtonGeom, self.coolToggleButtonGeom),
            boxRelief=None,
            pressEffect=1,
            clickSound=self.guiClickSound,
            rolloverSound=self.guiRolloverSound,
            command=executeFunction,
        )

        self.button.reparentTo(self.containerFrame)
        self.button.setPos(1.25, 0, 0.025)

        # The button on the thing.
        self.toggleButtonGeom.setScale(1)
        self.toggleButtonGeom.setPos(0.6, 0, -0.15)
        self.toggleButtonGeom.reparentTo(self.button)

        def animateToggle():
            if self.button['indicatorValue']:
                toggle_forward_interval = LerpPosInterval(
                    self.toggleButtonGeom, 0.15, (1.2, 0, -0.15), (0.6, 0, -0.15))
                toggle_forward_interval.start()
                activateCommand()
            else:
                toggle_back_interval = LerpPosInterval(
                    self.toggleButtonGeom, 0.15, (0.6, 0, -0.15), (1.2, 0, -0.15))
                toggle_back_interval.start()
                deactivateCommand()