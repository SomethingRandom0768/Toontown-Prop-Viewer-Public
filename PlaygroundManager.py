from direct.showbase.DirectObject import DirectObject
from panda3d.core import TextNode
from direct.directnotify import DirectNotifyGlobal

# GUI Imports
from .OptionsGUI import OptionsGUI, dynamicFrameGUI, dynamicFrameOnly
from direct.gui.DirectGui import *

# Playground imports
from playgrounds.ToontownCentral import ToontownCentral
from playgrounds.DonaldsDock import DonaldsDock
from playgrounds.DaisyGardens import DaisyGardens
from playgrounds.MinniesMelodyland import MinniesMelodyland
from playgrounds.TheBrrrgh import TheBrrrgh
from playgrounds.DonaldsDreamland import DonaldsDreamland
from playgrounds.GoofySpeedway import GoofySpeedway
from playgrounds.Cartoonival import Cartoonival
from playgrounds.ChipAndDales import ChipAndDales
from playgrounds.Kaboomberg import Kaboomberg

class PlaygroundManager(OptionsGUI):
    notify = DirectNotifyGlobal.directNotify.newCategory("PlaygroundManager")
    notify.setDebug(1)

    def __init__(self) -> None:
        super().__init__()
        self.buttonGeom = self.optionsGeom.find('**/ttr_t_gui_gen_buttons_squareButton')
        self.generatePlaygroundGUI()
        self.generateStreetsGUI()
        self.accept('l', self.showOrHideGUI)
        self.isGUIHidden = True
        self.playground = None
        self.generateShowPGGUIButton()
        self.hideGUI()
        self.notify.debug("Generated")
    
# GUI related stuff

    def generatePlaygroundGUI(self):
        '''Generates the GUI for the playground similar to the prop GUI'''

        playgroundGUIGeom = dynamicFrameOnly(25, 25)

        self.playgroundChooserGUI = DirectFrame(
            parent=aspect2d,
            geom=playgroundGUIGeom.geom,
            relief=None,
            pos=(-0.725,0,0.5),
            text = "Playground Chooser",
            text_scale=0.1,
            text_font=self.labelFont,
            text_fg=(0,1,1, 1),
            text_pos=(0.65,-0.1,0)
        )

        toontownCentralButton = DirectButton(
            parent=self.playgroundChooserGUI,
            geom=loader.loadModel('phase_3.5/models/props/mickeySZ.bam'),
            relief=None,
            scale=0.25,
            command = self.generateToontownCentral,
            pos=(0.2,0,-0.35),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        donaldsDockButton = DirectButton(
            parent=self.playgroundChooserGUI,
            geom=loader.loadModel('phase_4/models/props/donaldSZ.bam'),
            relief=None,
            scale=0.25,
            command = self.generateDonaldsDock,
            pos=(0.6,0,-0.35),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        daisyGardensButton = DirectButton(
            parent=self.playgroundChooserGUI,
            geom=loader.loadModel('phase_4/models/props/daisySZ.bam'),
            relief=None,
            scale=0.25,
            command = self.generateDaisyGardens,
            pos=(1,0,-0.35),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )
    
        minniesMelodyLandButton = DirectButton(
            parent=self.playgroundChooserGUI,
            geom=loader.loadModel('phase_4/models/props/minnieSZ.bam'),
            relief=None,
            scale=0.25,
            command = self.generateMinniesMelodyland,
            pos=(0.2,0,-0.65),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        theBrrrghButton = DirectButton(
            parent=self.playgroundChooserGUI, 
            geom=loader.loadModel('phase_4/models/props/plutoSZ.bam'),
            relief=None,
            scale=0.25,
            command=self.generateBrrrgh,
            pos=(0.6, 0, -0.65),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        donaldsDreamlandButton = DirectButton(
            parent=self.playgroundChooserGUI, 
            geom=loader.loadModel('phase_4/models/props/donald_DL_SZ.bam'),
            relief=None,
            scale=0.25,
            command=self.generateDonaldsDreamland,
            pos=(1, 0, -0.65),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        goofysSpeedwayButton = DirectButton(
            parent=self.playgroundChooserGUI, 
            geom=loader.loadModel('phase_4/models/props/goofySZ.bam'),
            relief=None,
            scale=0.25,
            command=self.generateGoofySpeedway,
            pos=(0.2, 0, -0.95),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        goofysSpeedwayButton = DirectButton(
            parent=self.playgroundChooserGUI, 
            geom=loader.loadModel('phase_4/models/props/goofySZ.bam'),
            relief=None,
            scale=0.25,
            command=self.generateGoofySpeedway,
            pos=(0.2, 0, -0.95),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        cartoonivalButton = DirectButton(
            parent=self.playgroundChooserGUI, 
            geom=loader.loadModel('phase_3.5/models/gui/toonfest_gui.bam'),
            relief=None,
            scale=0.25,
            command=self.generateCartoonival,
            pos=(0.2, 0, -0.95),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        chipAndDalesButton = DirectButton(
            parent=self.playgroundChooserGUI,
            geom=loader.loadModel('phase_6/models/golf/picnic_table.bam'),
            geom_scale=0.2,
            geom_pos=(0,0,-0.25),
            relief=None,
            scale=0.25,
            command=self.generateChipAndDales,
            pos=(0.6, 0, -0.95),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

        kaboombergButton = DirectButton(
            parent=self.playgroundChooserGUI,
            geom=loader.loadModel('phase_3.5/models/gui/ttr_m_gui_sbk_resistanceRank_icons.bam').find('**/icon_grp'),
            geom_scale=0.75,
            geom_pos=(0,0,0),
            relief=None,
            scale=0.25,
            command=self.generateKaboomberg,
            pos=(1, 0, -0.95),
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound
        )

    def showGUI(self):
        self.playgroundChooserGUI.show()
        self.streetsScrolledFrame.show()

    def hideGUI(self):
        self.playgroundChooserGUI.hide()
        self.streetsScrolledFrame.hide()
    
    def showOrHideGUI(self):
        if self.isGUIHidden:
            self.showGUI()
            self.showGUIButton['text'] = 'Hide PG\nMenu(L)'
            self.isGUIHidden = False
        else:
            self.isGUIHidden = True
            self.showGUIButton['text'] = 'Show PG\nMenu(L)'
            self.hideGUI()
    
    def destroyPlaygroundGUI(self):
        self.playgroundChooserGUI.destroy()
    
    def destroyPlayground(self):
        self.playground.cleanup()

    def generateShowPGGUIButton(self):
        self.showGUIButton = DirectButton(
            parent=aspect2d,
            geom=self.buttonGeom,
            relief=None,
            geom_scale=(0.5,0.5,0.75),
            text="Show PG\nMenu(L)",
            text_font=self.modalFont,
            text_scale=0.25,
            scale=0.25,
            pos=(-0.5,0,0.9),
            command=self.showOrHideGUI,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )

    def generateStreetsGUI(self):
        streetsDynamicFrame = dynamicFrameOnly(20, 20)

        self.streetsScrolledFrame = DirectScrolledFrame(
            geom=streetsDynamicFrame.geom,
            parent=aspect2d,
            frameSize = (0, 1, -1.05, -0.2),
            canvasSize = (0, 1, 0, 5),
            pos=(0.65,0,0.5),
            text="Streets",
            text_scale=0.2,
            text_font=self.labelFont,
            text_fg=(0,1,1, 1),
            text_pos=(0.5,-0.2,0),
            verticalScroll_incButton_relief=None,
            verticalScroll_decButton_relief=None,
            horizontalScroll_incButton_relief=None,
            horizontalScroll_decButton_relief=None,
            horizontalScroll_frameSize=(0,0,0,0),
            verticalScroll_geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_lineThick'),
            verticalScroll_geom_hpr=(0,0,90),
            verticalScroll_geom_scale=0.2,
            verticalScroll_geom_pos=(0.97,0,-0.65),
            verticalScroll_thumb_geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_slider1'),
            verticalScroll_thumb_geom_scale = 0.1,
            verticalScroll_thumb_geom_pos=(0.005,0,0),
            verticalScroll_thumb_relief=None,
            verticalScroll_thumb_frameSize=(0,0.5,0,0.5),
            verticalScroll_relief=None,
            relief=None,
            verticalScroll_thumb_rolloverSound=self.guiRolloverSound,
            verticalScroll_thumb_clickSound=self.guiClickSound

        )

        # Toontown Central
        loopyLaneButton = DirectButton(
            # geom=self.buttonGeom,
            geom_scale=0.25,
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0.24,0,4.85),
            text="Loopy Lane",
            text_font = self.labelFont,
            text_fg=(1, 0.5, 0, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateLoopyLane,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )
        punchlinePlaceButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 4.75),
            text="Punchline Place",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(1, 0.5, 0, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generatePunchlinePlace,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )
        sillyStreetButton = DirectButton(         
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 4.65),
            text="Silly Street",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(1, 0.5, 0, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateSillyStreet,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )
        

        # Donald's Dock
        barnacleBoulevardButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 4.5),
            text="Barnacle Boulevard",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0.6, 0.29, 0, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateBarnacleBoulevard,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )
        lighthouseLaneButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 4.4),
            text="Lighthouse Lane",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0.6, 0.29, 0, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateLighthouseLane,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )
        seaweedStreetButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 4.3),
            text="Seaweed Street",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0.6, 0.29, 0, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command = self.generateSeaweedStreet,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )

        # Daisy Gardens
        elmStreetButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 4.1),
            text="Elm Street",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0, 1, 0, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateElmStreet,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )
        mapleStreetButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 4),
            text="Maple Street",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0, 1, 0, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateMapleStreet,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )
        oakStreetButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 3.9),
            text="Oak Street",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0, 1, 0, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateOakStreet,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )

        # Minnies Melodyland
        altoAvenueButtonButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 3.7),
            text="Alto Avenue",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(1, 0.71, 0.75, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateAltoAvenue,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )    
        baritoneBoulevardButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 3.6),
            text="Baritone Boulevard",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(1, 0.71, 0.75, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateBaritoneBoulevard,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )
        tenorTerraceButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 3.5),
            text="Tenor Terrace",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(1, 0.71, 0.75, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateTenorTerrace,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )

        # # The Brrrgh
        sleetStreetButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 3.2),
            text="Sleet Street",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0.7, 1, 1, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateSleetStreet,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )    
        polarPlaceButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 3.1),
            text="Polar Place",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0.7, 1, 1, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generatePolarPlace,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )    
        walrusWayButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 3),
            text="Walrus Way",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0.7, 1, 1, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateWalrusWay,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )    

        # # Donald's Dreamland
        lullabyLaneButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 2.7),
            text="Lullaby Lane",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0.69, 0.149, 1, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generateLullabyLane,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )    
        pajamaPlaceButton = DirectButton(          
            # geom=self.buttonGeom,
            geom_scale=(0.25, 0.25, 0.25),
            parent = self.streetsScrolledFrame.getCanvas(),
            pos=(0, 0, 2.6),
            text="Pajama Place",
            text_font = self.labelFont,
            text_align=TextNode.ALeft,
            text_fg=(0.69, 0.149, 1, 1),
            text_scale=0.1,
            scale=0.75,
            relief=None,
            command=self.generatePajamaPlace,
            rolloverSound=self.guiRolloverSound,
            clickSound=self.guiClickSound 
        )    
      
    def deleteStreetsGUI(self):
        self.streetsScrolledFrame.destroy()

# Playground generations

    def generateToontownCentral(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = ToontownCentral(0, 0)

    def generateDonaldsDock(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DonaldsDock(0, 0)

    def generateDaisyGardens(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DaisyGardens(0, 0)
    
    def generateMinniesMelodyland(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = MinniesMelodyland(0, 0)
    
    def generateBrrrgh(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = TheBrrrgh(0, 0)
    
    def generateDonaldsDreamland(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DonaldsDreamland(0, 0)
    
    def generateGoofySpeedway(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = GoofySpeedway(0)

    def generateCartoonival(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = Cartoonival()

    def generateChipAndDales(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = ChipAndDales(0)
    
    def generateKaboomberg(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = Kaboomberg()

# Street generations

    # Toontown Central
    def generateLoopyLane(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = ToontownCentral(2200, 0)
    
    def generatePunchlinePlace(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = ToontownCentral(2300, 0)

    def generateSillyStreet(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = ToontownCentral(2100, 0)

    # Donald's Dock
    def generateLighthouseLane(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DonaldsDock(1300, 0)

    def generateSeaweedStreet(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DonaldsDock(1200, 0)
    
    def generateBarnacleBoulevard(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DonaldsDock(1100, 0)
    
    # Daisy Gardens

    def generateElmStreet(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DaisyGardens(5100, 0)
    
    def generateMapleStreet(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DaisyGardens(5200, 0)
    
    def generateOakStreet(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DaisyGardens(5300, 0)

    
    # Minnie's Melodyland

    def generateAltoAvenue(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = MinniesMelodyland(4100, 0)
    
    def generateBaritoneBoulevard(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = MinniesMelodyland(4200, 0)
    
    def generateTenorTerrace(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = MinniesMelodyland(4300, 0)
    
    # The Brrrgh

    def generateSleetStreet(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = TheBrrrgh(3200, 0)
    
    def generateWalrusWay(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = TheBrrrgh(3100, 0)
    
    def generatePolarPlace(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = TheBrrrgh(3300, 0)
    

    # Donalds Dreamland
    def generatePajamaPlace(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DonaldsDreamland(9200, 0)
    
    def generateLullabyLane(self):
        if self.playground != None:
            self.playground.cleanup()
            self.playground = None
        else:
            self.playground = DonaldsDreamland(9100, 0)
