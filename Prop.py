from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from .OptionsGUI import OptionsGUI, dynamicFrameOnly
from direct.directnotify import DirectNotifyGlobal
import os

class Prop(OptionsGUI):
    notify = DirectNotifyGlobal.directNotify.newCategory("Prop")
    notify.setDebug(1)

    '''A model that one can move around with a bunch of GUI around it to make it movable'''
    def __init__(self, modelPath) -> None:
        super().__init__()  
        self.model = loader.loadModel(modelPath)
        self.model.reparentTo(render)
        self.model.setPos(base.camera.getX(), base.camera.getY()+5, base.camera.getZ())
        self.generateHPRSlides()
        self.generatePropOptions()
        self.accept('b', self.cleanup)
        self.cameraLocked = 0
        self.notify.debug(modelPath + " loaded")


    def generatePropOptions(self):

        propOptionsGUI = dynamicFrameOnly(15,20)

        self.propOptionsFrame = DirectFrame(
            parent=aspect2d,
            geom=propOptionsGUI.geom,
            pos=(-1.75,0,-0.15),
            relief=None,
            scale=0.95
        )

        propOptionsFrameLabel = DirectLabel(
            parent=self.propOptionsFrame,
            text_font=self.labelFont,
            text_fg=(0,1,1, 1),
            scale=0.15,
            relief=None,
            pos=(0.5,0,-0.15),
            text="Options"
        )

        scaleSliderFrameLabel = DirectLabel(
            parent=self.propOptionsFrame,
            text_font=self.labelFont,
            text_fg=(0,1,1, 1),
            scale=0.072,
            relief=None,
            pos=(0.1,0,-0.275),
            text="Scale"
        )

        self.scaleSlider = DirectSlider(
            parent=self.propOptionsFrame,
            pos=(0.6,0,-0.25),
            geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_lineThick'),
            thumb_geom=self.sliderThumbGeom,
            thumb_geom_scale=0.15,
            geom_scale=(0.5,0.25,0.25),
            range=(1,2),
            scale=0.35,
            command=self.scaleProp,
            relief=None,
            thumb_rolloverSound=self.guiRolloverSound,
            thumb_clickSound=self.guiClickSound
        )

        self.lockCameraButton = DirectButton(
            parent=self.propOptionsFrame,
            geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_squareButton'),
            pos=(0.25,0,-0.5),
            geom_scale=0.35,
            scale=0.5,
            text_font=self.modalFont,
            text_scale=0.15,
            text='Lock Camera',
            command=self.cameraEnableOrDisable,
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        self.deletePropButton = DirectButton(
            parent=self.propOptionsFrame,
            geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_squareButton'),
            pos=(0.75,0,-0.5),
            geom_scale=0.35,
            scale=0.5,
            text_font=self.modalFont,
            text_scale=0.15,
            text='Delete Prop',
            command=self.cleanup,
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        self.showTexturesButton = DirectButton(
            parent=self.propOptionsFrame,
            geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_squareButton'),
            pos=(0.5,0,-0.7),
            geom_scale=0.35,
            scale=0.5,
            text_font=self.modalFont,
            text_scale=0.15,
            text='Print Textures',
            command=self.showTextures,
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )
        
    def generateHPRSlides(self):

        hprSliderGUI = dynamicFrameOnly(15,20)

        self.hprSliderFrame = DirectFrame(
        parent=aspect2d,
        geom=hprSliderGUI.geom,
        pos=(-1.75,0,0.75),
        relief=None,
        scale=0.95
    )

        scaleSliderFrameLabel = DirectLabel(
            parent=self.hprSliderFrame,
            text_font=self.labelFont,
            text_fg=(0,1,1, 1),
            scale=0.15,
            relief=None,
            pos=(0.5,0,-0.15),
            text="Rotation"
        )

        self.hHPRSlider = DirectSlider(
            parent=self.hprSliderFrame,
            pos=(0.5,0,-0.25),
            geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_lineThick'),
            thumb_geom=self.sliderThumbGeom,
            thumb_geom_scale=0.15,
            geom_scale=(0.5,0.25,0.25),
            range=(0,360),
            scale=0.5,
            relief=None,
            command=self.rotatePropH,
            thumb_rolloverSound=self.guiRolloverSound,
            thumb_clickSound=self.guiClickSound
        )

        self.pHPRSlider = DirectSlider(
            parent=self.hprSliderFrame,
            pos=(0.5,0,-0.5),
            geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_lineThick'),
            thumb_geom=self.sliderThumbGeom,
            thumb_geom_scale=0.15,
            geom_scale=(0.5,0.25,0.25),
            range=(0,360),
            scale=0.5,
            relief=None,
            command=self.rotatePropP,
            thumb_rolloverSound=self.guiRolloverSound,
            thumb_clickSound=self.guiClickSound
        )

        self.rHPRSlider = DirectSlider(
            parent=self.hprSliderFrame,
            pos=(0.5,0,-0.75),
            geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_lineThick'),
            thumb_geom=self.sliderThumbGeom,
            thumb_geom_scale=0.15,
            geom_scale=(0.5,0.25,0.25),
            range=(0,360),
            scale=0.5,
            relief=None,
            command=self.rotatePropR,
            thumb_rolloverSound=self.guiRolloverSound,
            thumb_clickSound=self.guiClickSound
        )

    def deletePropOptions(self):
        self.propOptionsFrame.removeNode()

    def cleanup(self):
        self.propOptionsFrame.destroy()
        self.hprSliderFrame.destroy()
        self.model.removeNode()
        self.ignoreAll()

    def cameraEnableOrDisable(self):
        if self.cameraLocked:
            self.cameraLocked = 0
            base.enableMouse()
            self.lockCameraButton['text'] = 'Lock Camera'
            self.lockCameraButton['geom_scale'] = 0.35
            self.notify.debug("Camera Unlocked")
        else:
            self.cameraLocked = 1
            base.disableMouse()
            self.lockCameraButton['text'] = 'Unlock Camera'
            self.lockCameraButton['geom_scale'] = 0.375
            self.notify.debug("Camera Locked")

# Prop Functions (activated by Options)

    def showTextures(self):
        text = ""
        for texture in self.model.findAllTextures():
            location = str.split( str(texture.get_filename()), os.getcwd() + "/")
            text += location[1] + "\n"
        self.notify.debug("This is the model's textures:\n" + text)
        # self.notify.debug(text)
        print("\n")

    def scaleProp(self):
        self.model.setScale(self.scaleSlider['value'])

    def rotatePropH(self):
        self.model.setH(self.hHPRSlider['value'])

    def rotatePropP(self):
        self.model.setP(self.pHPRSlider['value'])

    def rotatePropR(self):
        self.model.setR(self.rHPRSlider['value'])