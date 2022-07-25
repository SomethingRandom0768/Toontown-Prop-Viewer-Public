from .Prop import Prop
from .OptionsGUI import OptionsGUI, dynamicFrameGUI, dynamicFrameOnly
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.LerpInterval import *
from panda3d.core import *
from panda3d.core import Thread
from direct.task import *
import glob

class PropGUI(OptionsGUI):
    def __init__(self, phaseDirectory):
        '''Generates a dynamic frame and then populates it with models.'''
        super().__init__()

        phaseDirectory = phaseDirectory
        # Variables
        self.buttonGeom = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_squareButton')
        self.isGUIHidden = True
        self.currentPhase = ""
        self.containerButtons = []

        # Events
        self.accept('wheel_up', self.scrollFrameUp)
        self.accept('wheel_down', self.scrollFrameDown)
        self.accept('k', self.showOrHideGUI)

        # Functions
        self.generatePropFrame()
        taskMgr.add(self.generatePropGUI())
        self.generatePropList(phaseDirectory)
        self.generateFolderButtonGUI()
        self.generateShowPropGUIButton()
        self.generatePhaseButtons()

    def generatePropFrame(self):
        propFrame = dynamicFrameOnly(25, 31)

        self.selectionPropMainFrame = DirectFrame(
            parent=aspect2d,
            geom=propFrame.geom,
            geom_pos=(-0.85,0,0.75),
            relief=None
        )

        self.selectionFrame = DirectScrolledFrame(
            parent=self.selectionPropMainFrame,
            pos=(-0.15, 0, -0),
            verticalScroll_incButton_relief=None,
            verticalScroll_decButton_relief=None,
            verticalScroll_geom = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_lineThick'),
            verticalScroll_relief=None,
            verticalScroll_geom_hpr=(0,0,90),
            verticalScroll_geom_scale=(0.2, 0.25, 0.2),
            verticalScroll_geom_pos=(0.714,0,0.05),
            verticalScroll_thumb_geom = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_slider1'),
            verticalScroll_thumb_geom_scale = 0.1,
            horizontalScroll_relief=None,
            horizontalScroll_frameSize=(0,0,0,0),
            horizontalScroll_thumb_relief=None,
            horizontalScroll_incButton_relief=None,
            horizontalScroll_decButton_relief=None,
            frameSize=(-0.75,0.75,-0.5,0.5),
            canvasSize=(-1, 1, -20, 1),
            relief=None,
            verticalScroll_thumb_rolloverSound=self.guiRolloverSound,
            verticalScroll_thumb_clickSound=self.guiClickSound
    )

        propFrameLabel = DirectLabel(
            text_font=self.labelFont,
            parent=self.selectionFrame,
            text="Prop Chooser",
            text_scale=0.20,
            text_fg=(0,1,1, 1),
            relief=None,
            pos=(0.1,0,0.55)
        )

        self.selectionPropMainFrame.hide()

    async def generatePropGUI(self):



        propListLength = len(self.propList)
        self.propList.sort()

        xCounter = 0
        yCounter = 0
        i = 0
        loaderCounter = 0
        objectID = 0 # To keep track of all the objects.

        # Useful for figuring out invisible models.
        # for prop in self.propList:
        #     print(prop)

        for i in range (0, propListLength):
            model = await loader.loadModel(self.propList[i], blocking=False)
            # To make sure the model can be seen without clipping issues
            model.setDepthTest(1)
            model.setDepthWrite(1)

            containerGUI = dynamicFrameOnly(3, 3)

            modelFrame = DirectButton(
            parent=self.selectionFrame.getCanvas(),
            geom=containerGUI.geom,
            geom_pos=(0.025, 0, 0.2),
            pos= (-0.95 + xCounter * 0.35, 0, 0.75 - 0.3 * yCounter),
            frameColor=(1,1,1,1),
            frameSize=(0, 1.25, 0, 0.25),
            relief=None,
            command=self.sendProp,
            extraArgs=[objectID],
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )
        
            pitch = modelFrame.attachNewNode('pitch')
            rotate = pitch.attachNewNode('rotate')
            scale = rotate.attachNewNode('scale')
            pitch.setPos(modelFrame.getCenter()[0])

            model.reparentTo(scale)
            model.setScale(0.1)

            try:
                bMin,bMax = model.getTightBounds()
                center = (bMin + bMax)/2.0
                model.setPos(-center[0], -center[1], -center[2])
                pitch.setP(20)

                # COMMENT THIS OUT FOR LINUX, AND UNCOMMENT FOR WINDOWS
                pitch.setX(0.125)
                pitch.setZ(0.1)

                bMin,bMax = pitch.getTightBounds()
                center = (bMin + bMax)/2.0
                corner = Vec3(bMax - center)
                scale.setScale(0.1/max(corner[0],corner[1],corner[2]))
            except:
                pass

            rotation = LerpHprInterval(model, 10, (360,0,0), (0,0,0))
            rotation.loop()

            xCounter += 1
            if i % 4 == 0:
                yCounter += 1
                xCounter = 0 

            objectID+=1
            self.propModelList.append(model) 
            self.containerButtons.append(modelFrame)

    def generatePropList(self, phaseDirectory):
        files = glob.glob( phaseDirectory + "/*")
        self.propList = []
        self.propModelList = []

        # Just adding to the list so we can use an iterator number
        for file in files:
            self.propList.append(file)
        
        self.propList.sort()

        self.removeAnimations()
        
    def removeAnimations(self):
        for prop in self.propList:
            try:
                model = loader.loadModel(prop)
                modelNodes = model.getChildren()

                for node in modelNodes:
                    pandaNodes = node.getNodes()

                    for innerNode in pandaNodes:
                        if 'Anim' in str(type(innerNode)):
                            self.propList.remove(prop)
                        else:
                            pass
                model.removeNode()
            except:
                pass

        # print("Here are the props:\n")
        # for prop in self.propList:
        #     print(prop)

    def generateFolderButtonGUI(self):
        phaseButton = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_squareButton')

        containerForPhaseButtons = dynamicFrameOnly(27, 15)

        self.phaseButtonContainerFrame = DirectFrame(
            parent=aspect2d,
            geom=containerForPhaseButtons.geom,
            pos=(0.95,0,0.75),
            relief=None
        )

        phaseThreeButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.2,0,-0.175),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseThreeButtons,
        )

        phaseThreeLabel = DirectLabel(
            text='Phase 3',
            parent=phaseThreeButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )

        phaseThreePointFiveButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.2,0,-0.35),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseThreePointFiveButtons,
        )

        phaseThreePointFiveLabel = DirectLabel(
            text='Phase 3.5',
            parent=phaseThreePointFiveButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )

        phaseFourButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.6,0,-0.35),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseFourButtons,
        )

        phaseFourLabel = DirectLabel(
            text='Phase 4',
            parent=phaseFourButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )

        phaseFiveButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.2,0,-0.525),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseFiveButtons,
        )

        phaseFiveLabel = DirectLabel(
            text='Phase 5',
            parent=phaseFiveButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )

        phaseFivePointFiveButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.6,0,-0.525),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseFivePointFiveButtons,
        )

        phaseFivePointFiveLabel = DirectLabel(
            text='Phase 5.5',
            parent=phaseFivePointFiveButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )

        phaseSixButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.2,0,-0.7),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseSixButtons,
        )

        phaseSixLabel = DirectLabel(
            text='Phase 6',
            parent=phaseSixButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )   

        phaseSevenButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.6,0,-0.7),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseSevenButtons,
        )

        phaseSevenLabel = DirectLabel(
            text='Phase 7',
            parent=phaseSevenButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )   

        phaseEightButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.2,0,-0.9),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseEightButtons,
        )

        phaseEightLabel = DirectLabel(
            text='Phase 8',
            parent=phaseEightButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )   
        
        phaseNineButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.6,0,-0.9),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseNineButtons,
        )

        phaseNineLabel = DirectLabel(
            text='Phase 9',
            parent=phaseNineButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )   

        phaseTenButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.2,0,-1.1),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseTenButtons,
        )

        phaseTenLabel = DirectLabel(
            text='Phase 10',
            parent=phaseTenButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )   

        phaseElevenButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.6,0,-1.1),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseElevenButtons,
        )

        phaseElevenLabel = DirectLabel(
            text='Phase 11',
            parent=phaseElevenButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )   

        phaseTwelveButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.2,0,-1.3),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseTwelveButtons,
        )

        phaseTwelveLabel = DirectLabel(
            text='Phase 12',
            parent=phaseTwelveButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        )

        phaseThirteenButton = DirectButton(
            geom=phaseButton,
            geom_scale=0.75,
            parent=self.phaseButtonContainerFrame,
            scale=0.2,
            pos=(0.6,0,-1.3),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.generatePhaseThirteenButtons,
        )

        phaseThirteenLabel = DirectLabel(
            text='Phase 13',
            parent=phaseThirteenButton,
            text_font=self.modalFont,
            text_scale=0.33,
            pos=(0,0,-0.06),
            relief=None
        ) 

        self.phaseButtonContainerFrame.hide()

    def destroyFolderButtonGUI(self):
        self.phaseButtonContainerFrame.removeNode()

    def cleanup(self):
        for propModel in self.propModelList:
            propModel.removeNode()
        for button in self.containerButtons:
            button.destroy()
        self.hidePhaseButtons()

    def repopulate(self, phaseDirectory):
        self.cleanup()
        self.generatePropList(phaseDirectory)
        taskMgr.add(self.generatePropGUI()) 

    def sendProp(self, propID):
        '''Sends the prop model to the Prop Generator'''
        newProp = Prop(self.propList[propID])
        self.showOrHideGUI()
        
    def hideGUI(self):
        self.selectionPropMainFrame.hide()
        self.phaseButtonContainerFrame.hide()
    
    def showGUI(self):
        self.selectionPropMainFrame.show()
        self.phaseButtonContainerFrame.show()        

    def showOrHideGUI(self):
        if self.isGUIHidden:
            self.showGUI()
            self.isGUIHidden = False
            self.showGUIButton['text'] = 'Hide Props\nMenu(K)'
        else:
            self.isGUIHidden = True
            self.showGUIButton['text'] = 'Show Props\nMenu(K)'
            self.hideGUI()
        
        if self.currentPhase == "phase_3":
            self.phaseThreeDynamicFrame.hide()
        elif self.currentPhase == "phase_3.5":
            self.phaseThreePointFiveDynamicFrame.hide()
        elif self.currentPhase == "phase_4":
            self.phaseFourDynamicFrame.hide()
        elif self.currentPhase == "phase_5":
            self.phaseFiveDynamicFrame.hide()
        elif self.currentPhase == "phase_5.5":
            self.phaseFivePointFiveDynamicFrame.hide()
        elif self.currentPhase == "phase_6":
            self.phaseSixDynamicFrame.hide()
        elif self.currentPhase == "phase_7":
            self.phaseSevenDynamicFrame.hide()
        elif self.currentPhase == "phase_8":
            self.phaseEightDynamicFrame.hide()
        elif self.currentPhase == "phase_9":
            self.phaseNineDynamicFrame.hide()
        elif self.currentPhase == "phase_10":
            self.phaseTenDynamicFrame.hide()
        elif self.currentPhase == "phase_11":
            self.phaseElevenDynamicFrame.hide()
        elif self.currentPhase == "phase_12":
            self.phaseTwelveDynamicFrame.hide()
        elif self.currentPhase == "phase_13":
            self.phaseThirteenDynamicFrame.hide()
        else:
            pass
        
    def generateShowPropGUIButton(self):
        self.showGUIButton = DirectButton(
            parent=aspect2d,
            geom=self.buttonGeom,
            relief=None,
            geom_scale=(0.5,0.5,0.75),
            text="Show Props\nMenu(K)",
            text_font=self.modalFont,
            text_scale=0.25,
            scale=0.25,
            pos=(0,0,0.9),
            command=self.showOrHideGUI,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

    def scrollFrameDown(self):
        self.selectionFrame['verticalScroll_value']+=0.05

    def scrollFrameUp(self):
        self.selectionFrame['verticalScroll_value']-=0.05 
    

# This is for each phase file.


# Generations
    def generatePhaseButtons(self):
        '''Generates the phase buttons and hides them.'''
        self.generatePhaseThreeButtons()
        self.generatePhaseThreePointFiveButtons()
        self.generatePhaseFourButtons()
        self.generatePhaseFiveButtons()
        self.generatePhaseFivePointFiveButtons()
        self.generatePhaseSixButtons()
        self.generatePhaseSevenButtons()
        self.generatePhaseEightButtons()
        self.generatePhaseNineButtons()
        self.generatePhaseTenButtons()
        self.generatePhaseElevenButtons()
        self.generatePhaseTwelveButtons()
        self.generatePhaseThirteenButtons()

        self.phaseThreeDynamicFrame.hide()
        self.phaseThreePointFiveDynamicFrame.hide()
        self.phaseFourDynamicFrame.hide()
        self.phaseFiveDynamicFrame.hide()
        self.phaseFivePointFiveDynamicFrame.hide()
        self.phaseSixDynamicFrame.hide()
        self.phaseSevenDynamicFrame.hide()
        self.phaseEightDynamicFrame.hide()
        self.phaseNineDynamicFrame.hide()
        self.phaseTenDynamicFrame.hide()
        self.phaseElevenDynamicFrame.hide()
        self.phaseTwelveDynamicFrame.hide()
        self.phaseThirteenDynamicFrame.hide()
    
    def generatePhaseThreeButtons(self):
        self.currentPhase = "phase_3"
        phaseThreeDynamicFrame = dynamicFrameOnly(15, 15)

        self.phaseThreeDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseThreeCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThreeDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_3/models/char']
        )

        phaseThreeGUIButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThreeDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="GUI",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_3/models/gui']
        )

        phaseThreeMakeAToonButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThreeDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="MakeAToon",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_3/models/makeatoon']
        )

        phaseThreeMiscButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThreeDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Misc",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_3/models/misc']
        )

        phaseThreePropsButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThreeDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.6),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Props",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_3/models/props']
        )

    def generatePhaseThreePointFiveButtons(self):
        self.currentPhase = "phase_3.5"
        phaseThreeDynamicFrame = dynamicFrameOnly(15, 15)

        self.phaseThreePointFiveDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseThreePointFiveCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThreePointFiveDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_3.5/models/char']
        )

        phaseThreePointFiveGUIButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThreePointFiveDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="GUI",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_3.5/models/gui']
        )

        phaseThreePointFiveModulesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThreePointFiveDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Modules",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_3.5/models/modules']
        )

        phaseThreePointFivePropsButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThreePointFiveDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Props",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_3.5/models/props']
        )

    def generatePhaseFourButtons(self):
        self.currentPhase = "phase_4"
        phaseThreeDynamicFrame = dynamicFrameOnly(25, 15)

        self.phaseFourDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseFourAccessoriesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Accessories",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/accessories']
        )

        phaseFourCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/char']
        )

        phaseFourCogHQButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Cog HQ",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/CogHQ']
        )

        phaseFourEstateButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Estates",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/estate']
        )

        phaseFourEventsButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.6),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Events",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/events']
        )

        phaseFourGUIButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.6),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="GUI",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/gui']
        )

        phaseFourKartingButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.8),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Karting",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/karting']
        )

        phaseFourMinigamesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.8),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Minigames",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/minigames']
        )

        phaseFourModulesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-1),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Modules",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/modules']
        )

        phaseFourPartiesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-1),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Parties",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/parties']
        )

        phaseFourPropsButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-1.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Props",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/props']
        )

        phaseFourQuestMapButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFourDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-1.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Quest Map",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_4/models/questmap']
        )

    def generatePhaseFiveButtons(self):
        self.currentPhase = "phase_5"
        phaseThreeDynamicFrame = dynamicFrameOnly(15, 15)

        self.phaseFiveDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseFiveCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFiveDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5/models/char']
        )

        phaseFiveCogDoButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFiveDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Field Offices",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5/models/cogdominium']
        )

        phaseFiveGUIButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFiveDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="GUI",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5/models/gui']
        )

        phaseFiveModulesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFiveDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Modules",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5/models/modules']
        )

        phaseFivePropsButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFiveDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.6),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Props",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5/models/props']
        )

    def generatePhaseFivePointFiveButtons(self):
        self.currentPhase = "phase_5.5"
        phaseThreeDynamicFrame = dynamicFrameOnly(15, 15)

        self.phaseFivePointFiveDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseFivePointFiveCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFivePointFiveDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5.5/models/char']
        )

        phaseFivePointFiveEstateButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFivePointFiveDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Estate",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5.5/models/estate']
        )

        phaseFivePointFiveGUIButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFivePointFiveDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="GUI",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5.5/models/gui']
        )

        phaseFivePointFivePartiesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFivePointFiveDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Parties",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5.5/models/parties']
        )

        phaseFivePointFivePropsButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseFivePointFiveDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.6),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Props",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_5.5/models/props']
        )

    def generatePhaseSixButtons(self):
        self.currentPhase = "phase_6"
        phaseThreeDynamicFrame = dynamicFrameOnly(17, 15)

        self.phaseSixDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseSixCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSixDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_6/models/char']
        )

        phaseSixCogHQButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSixDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Cog HQ",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_6/models/cogHQ']
        )

        phaseSixEventsButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSixDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Events",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_6/models/events']
        )

        phaseSixGolfButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSixDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Golf",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_6/models/golf']
        )

        phaseSixGUIButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSixDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.6),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="GUI",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_6/models/gui']
        )

        phaseSixKartingButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSixDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.6),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Karting",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_6/models/karting']
        )

        phaseSixModulesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSixDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.8),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Modules",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_6/models/modules']
        )

        phaseSixPropsButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSixDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.8),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Props",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_6/models/props']
        )

    def generatePhaseSevenButtons(self):
        self.currentPhase = "phase_7"
        phaseThreeDynamicFrame = dynamicFrameOnly(5, 15)

        self.phaseSevenDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseSevenCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSevenDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_7/models/char']
        )

        phaseSevenModulesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseSevenDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Modules",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_7/models/modules']
        )

    def generatePhaseEightButtons(self):
        self.currentPhase = "phase_8"
        phaseThreeDynamicFrame = dynamicFrameOnly(9, 15)

        self.phaseEightDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseEightCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseEightDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_8/models/char']
        )

        phaseEightMinigamesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseEightDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Minigames",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_8/models/minigames']
        )

        phaseEightModulesButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseEightDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Modules",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_8/models/modules']
        )

        phaseEightPropsButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseEightDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Props",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_8/models/props']
        )

    def generatePhaseNineButtons(self):
        self.currentPhase = "phase_9"
        phaseThreeDynamicFrame = dynamicFrameOnly(9, 15)

        self.phaseNineDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseNineCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseNineDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_9/models/char']
        )

        phaseNineCogHQButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseNineDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Cog HQ",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_9/models/cogHQ']
        )

        phaseNineGUIButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseNineDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="GUI",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_9/models/gui']
        )

    def generatePhaseTenButtons(self):
        self.currentPhase = "phase_10"
        phaseThreeDynamicFrame = dynamicFrameOnly(9, 15)

        self.phaseTenDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseTenCashbotHQButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseTenDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Cashbot HQ",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_10/models/cashbotHQ']
        )

        phaseTenCharButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseTenDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_10/models/char']
        )

        phaseTenCogHQButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseTenDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.4),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Cog HQ",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_10/models/cogHQ']
        )

    def generatePhaseElevenButtons(self):
        self.currentPhase = "phase_11"
        phaseThreeDynamicFrame = dynamicFrameOnly(9, 15)

        self.phaseElevenDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseElevenCharFrame = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseElevenDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_11/models/char']
        )

        phaseElevenLawbotHQFrame = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseElevenDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Lawbot HQ",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_11/models/lawbotHQ']
        )

    def generatePhaseTwelveButtons(self):
        self.currentPhase = "phase_12"
        phaseThreeDynamicFrame = dynamicFrameOnly(9, 15)

        self.phaseTwelveDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseTwelveBossbotHQFrame = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseTwelveDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Bossbot HQ",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_12/models/bossbotHQ']
        )

        phaseTwelveCharFrame = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseTwelveDynamicFrame,
            scale=0.2,
            pos=(0.6,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Char",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_12/models/char']
        )

    def generatePhaseThirteenButtons(self):
        self.currentPhase = "phase_13"
        phaseThreeDynamicFrame = dynamicFrameOnly(9, 15)

        self.phaseThirteenDynamicFrame = DirectFrame(
            parent=aspect2d,
            geom=phaseThreeDynamicFrame.geom,
            pos=(-1.75,0,0.5),
            relief=None

        )

        phaseThirteenEstateButton = DirectButton(
            geom=self.buttonGeom,
            geom_scale=0.75,
            parent=self.phaseThirteenDynamicFrame,
            scale=0.2,
            pos=(0.2,0,-0.2),
            relief=None,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound,
            command=self.repopulate,
            text="Estates",
            text_font=self.modalFont,
            text_scale=0.4,
            text_pos=(0,-0.1,0),
            extraArgs=['phase_13/models/estate']
        )

# Deletions
    def deletePhaseThreeButtons(self):
        self.phaseThreeDynamicFrame.destroy()

    def deletePhaseThreePointFiveButtons(self):
        self.phaseThreePointFiveDynamicFrame.destroy()

    def deletePhaseFourButtons(self):
        self.phaseFourDynamicFrame.destroy()
    
    def deletePhaseFiveButtons(self):
        self.phaseFiveDynamicFrame.destroy()

    def deletePhaseFivePointFiveButtons(self):
        self.phaseFivePointFiveDynamicFrame.destroy()
    
    def deletePhaseSixButtons(self):
        self.phaseSixDynamicFrame.destroy()
    
    def deletePhaseSevenButtons(self):
        self.phaseSevenDynamicFrame.destroy()

    def deletePhaseEightButtons(self):
        self.phaseEightDynamicFrame.destroy()

    def deletePhaseNineButtons(self):
        self.phaseNineDynamicFrame.destroy()

    def deletePhaseTenButtons(self):
        self.phaseTenDynamicFrame.destroy()

    def deletePhaseElevenButtons(self):
        self.phaseElevenDynamicFrame.destroy()

# Other Methods

    def hidePhaseButtons(self):
        '''Useful when pressing one of the phase buttons.'''
        self.phaseThreeDynamicFrame.hide()
        self.phaseThreePointFiveDynamicFrame.hide()
        self.phaseFourDynamicFrame.hide()
        self.phaseFiveDynamicFrame.hide()
        self.phaseFivePointFiveDynamicFrame.hide()
        self.phaseSixDynamicFrame.hide()
        self.phaseSevenDynamicFrame.hide()
        self.phaseEightDynamicFrame.hide()
        self.phaseNineDynamicFrame.hide()
        self.phaseTenDynamicFrame.hide()
        self.phaseElevenDynamicFrame.hide()
        self.phaseTwelveDynamicFrame.hide()
        self.phaseThirteenDynamicFrame.hide()

