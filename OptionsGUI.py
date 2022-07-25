from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from panda3d.core import *

class OptionsGUI(DirectObject):
    '''A class that sets up all the resources needed for GUI '''
    def __init__(self) -> object:
        self.optionsGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam')
        self.dynamicFrameGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_dynamicFrame.bam')
        self.labelFont = loader.loadFont('phase_3/fonts/MickeyFontMaximum.bam')
        self.modalFont = loader.loadFont('phase_3/fonts/ImpressBT.ttf')
        self.gagInventoryGUI = loader.loadModel('phase_3.5/models/gui/inventory_icons.bam')
        self.sliderGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam').find('**/ttr_t_gui_gen_buttons_lineSkinny')
        self.sliderThumbGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam').find('**/ttr_t_gui_gen_buttons_slider2')
        self.selectionFrameThumbGeom = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons.bam').find('**/ttr_t_gui_gen_buttons_slider1')
        self.guiClickSound = loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg')
        self.guiRolloverSound = loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg')

class dynamicFrameGUI(OptionsGUI):
    """A dynamic frame that resizes based on the height and width."""
    def __init__(self, parent, xPosition, yPosition, height=5, width=2) -> DirectObject:
        super().__init__()  
        self.mainFrame = self.generateMainFrame(parent, xPosition, yPosition, height, width) # This is the main GUI that has everything. 
        
    def generateMainFrame(self, parent, x_position, y_position,  height, width):
        '''Generates the dynamic frame that contains all of the objects'''
        topLeftModel = self.dynamicFrameGeom.find('**/topLeft')
        topMiddleModel = self.dynamicFrameGeom.find('**/topMiddle')
        topRightModel = self.dynamicFrameGeom.find('**/topRight')
        centerLeftModel = self.dynamicFrameGeom.find('**/centerLeft')
        centerMiddleModel = self.dynamicFrameGeom.find('**/centerMiddle')
        centerRightModel = self.dynamicFrameGeom.find('**/centerRight')
        bottomLeftModel = self.dynamicFrameGeom.find('**/bottomLeft')
        bottomMiddleModel = self.dynamicFrameGeom.find('**/bottomMiddle')
        bottomRightModel = self.dynamicFrameGeom.find('**/bottomRight')

        self.selectableDynamicFrame = NodePath('selectableFrame')

        topPiece = NodePath('top_half')

        # The Top Left piece
        topLeftModel.setScale(0.05)
        topLeftModel.reparentTo(topPiece)
        topLeftModel.setPos(0, 0, 0)

        # The top middle piece
        topMiddleModel.setScale(0.05)
        topMiddleModel.reparentTo(topPiece)
        topMiddleModel.setPos(topLeftModel.getX() + 0.05, 0, topLeftModel.getZ())

        # The Top Middle repetitions
        for i in range(1, width):
            self.top_center_copy = topMiddleModel.copyTo(topPiece)
            self.top_center_copy.setPos(topMiddleModel.getX()+(0.05*i), 0, 0)

        # The Top Right piece
        topRightModel.setScale(0.05)
        topRightModel.reparentTo(topPiece)
        topRightModel.setPos(topMiddleModel.getX()+(0.05*width), 0, 0)

        topPiece.flattenStrong()
        topPiece.reparentTo(self.selectableDynamicFrame)
        topPiece.setPos(0, 0, 0)
        # Let's make a node that we can duplicate.

        middlePiece = NodePath('middle_half')
        middlePiece.reparentTo(self.selectableDynamicFrame)
        middlePiece.setPos(0, 0, -0.05)

        centerLeftModel.setScale(0.05)
        centerLeftModel.reparentTo(middlePiece)
        centerLeftModel.setPos(0, 0, 0)

        centerMiddleModel.setScale(0.05)
        centerMiddleModel.reparentTo(middlePiece)
        centerMiddleModel.setPos(0.05, 0, 0)

        # The Center Middle repetitions
        for i in range(1, width+1):
            self.center_middle_copy = centerMiddleModel.copyTo(middlePiece)
            self.center_middle_copy.setPos(0.05*i, 0, 0)

        centerRightModel.setScale(0.05)
        centerRightModel.reparentTo(middlePiece)
        centerRightModel.setPos((width+1)*0.05, 0, 0)

        # Now let's duplicate the amount of times the thing is made.

        middlePiece.flattenStrong()

        for i in range(1, height):
            self.middlePiece_copy = middlePiece.copyTo(
                self.selectableDynamicFrame)
            self.middlePiece_copy.setPos(0, 0, (i * -0.05))

        bottom_piece = NodePath('bottom_half')
        bottom_piece.reparentTo(self.selectableDynamicFrame)
        bottom_piece.setPos(0, 0, height * -0.05)

        bottomLeftModel.setScale(0.05)
        bottomLeftModel.reparentTo(bottom_piece)
        bottomLeftModel.setPos(0, 0, -0.05)

        bottomMiddleModel.setScale(0.05)
        bottomMiddleModel.reparentTo(bottom_piece)
        bottomMiddleModel.setPos(0.05, 0, -0.05)

        # The Bottom Middle repetitions
        for i in range(1, width+1):
            self.bottom_middle_copy = bottomMiddleModel.copyTo(bottom_piece)
            self.bottom_middle_copy.setPos((0.05*i), 0, -0.05)

        # self.selectableDynamicFrame.ls()
        bottomRightModel.setScale(0.05)
        bottomRightModel.reparentTo(bottom_piece)
        bottomRightModel.setPos((width+1)*0.05, 0, -0.05)

        bottom_piece.flattenStrong()

        self.selectablesFrame = DirectFrame(
            geom=self.selectableDynamicFrame,
            parent=parent,
            pos=(x_position, 0, y_position),
            relief=None,
        )

        self.selectableScrollFrame = DirectScrolledFrame(
            parent=self.selectablesFrame,
            frameSize=(0, width*0.052, -0.4, 0),
            canvasSize=(0, 1.5, 5, 0),

            verticalScroll_incButton_relief=None,
            verticalScroll_decButton_relief=None,
            verticalScroll_range=(0, 0.5),
            verticalScroll_value=0,
            verticalScroll_manageButtons=True,
            verticalScroll_resizeThumb=True,
            verticalScroll_relief=None,
            verticalScroll_thumb_relief=None,
            verticalScroll_thumb_geom=self.selectionFrameThumbGeom,
            verticalScroll_thumb_geom_scale=0.05,
            verticalScroll_thumb_geom_pos=(0, 0, 0),

            verticalScroll_geom=self.sliderGeom,
            verticalScroll_geom_scale=0.085,
            verticalScroll_geom_pos=(width*0.049, 0, -0.175),
            verticalScroll_geom_hpr=(0, 0, 90),

            horizontalScroll_relief=None,
            horizontalScroll_thumb_relief=None,
            horizontalScroll_incButton_relief=None,
            horizontalScroll_decButton_relief=None,
            scrollBarWidth=0.05,
            relief=None,
        )

class dynamicFrameOnly(OptionsGUI):
    '''A dynamic frame that only returns the nodepath.'''
    def __init__(self, height, width) -> object:
        super().__init__()

        self.geom = self.generateOnlyFrame(height, width)


    def generateOnlyFrame(self, height, width):
        '''Generates the dynamic frame that contains all of the objects'''
        topLeftModel = self.dynamicFrameGeom.find('**/topLeft')
        topMiddleModel = self.dynamicFrameGeom.find('**/topMiddle')
        topRightModel = self.dynamicFrameGeom.find('**/topRight')
        centerLeftModel = self.dynamicFrameGeom.find('**/centerLeft')
        centerMiddleModel = self.dynamicFrameGeom.find('**/centerMiddle')
        centerRightModel = self.dynamicFrameGeom.find('**/centerRight')
        bottomLeftModel = self.dynamicFrameGeom.find('**/bottomLeft')
        bottomMiddleModel = self.dynamicFrameGeom.find('**/bottomMiddle')
        bottomRightModel = self.dynamicFrameGeom.find('**/bottomRight')

        self.selectableDynamicFrame = NodePath('selectableFrame')

        topPiece = NodePath('top_half')

        # The Top Left piece
        topLeftModel.setScale(0.05)
        topLeftModel.reparentTo(topPiece)
        topLeftModel.setPos(0, 0, 0)

        # The top middle piece
        topMiddleModel.setScale(0.05)
        topMiddleModel.reparentTo(topPiece)
        topMiddleModel.setPos(topLeftModel.getX() + 0.05, 0, topLeftModel.getZ())

        # The Top Middle repetitions
        for i in range(1, width):
            self.top_center_copy = topMiddleModel.copyTo(topPiece)
            self.top_center_copy.setPos(topMiddleModel.getX()+(0.05*i), 0, 0)

        # The Top Right piece
        topRightModel.setScale(0.05)
        topRightModel.reparentTo(topPiece)
        topRightModel.setPos(topMiddleModel.getX()+(0.05*width), 0, 0)

        topPiece.flattenStrong()
        topPiece.reparentTo(self.selectableDynamicFrame)
        topPiece.setPos(0, 0, 0)
        # Let's make a node that we can duplicate.

        middlePiece = NodePath('middle_half')
        middlePiece.reparentTo(self.selectableDynamicFrame)
        middlePiece.setPos(0, 0, -0.05)

        centerLeftModel.setScale(0.05)
        centerLeftModel.reparentTo(middlePiece)
        centerLeftModel.setPos(0, 0, 0)

        centerMiddleModel.setScale(0.05)
        centerMiddleModel.reparentTo(middlePiece)
        centerMiddleModel.setPos(0.05, 0, 0)

        # The Center Middle repetitions
        for i in range(1, width+1):
            self.center_middle_copy = centerMiddleModel.copyTo(middlePiece)
            self.center_middle_copy.setPos(0.05*i, 0, 0)

        centerRightModel.setScale(0.05)
        centerRightModel.reparentTo(middlePiece)
        centerRightModel.setPos((width+1)*0.05, 0, 0)

        # Now let's duplicate the amount of times the thing is made.

        middlePiece.flattenStrong()

        for i in range(1, height):
            self.middlePiece_copy = middlePiece.copyTo(
                self.selectableDynamicFrame)
            self.middlePiece_copy.setPos(0, 0, (i * -0.05))

        bottom_piece = NodePath('bottom_half')
        bottom_piece.reparentTo(self.selectableDynamicFrame)
        bottom_piece.setPos(0, 0, height * -0.05)

        bottomLeftModel.setScale(0.05)
        bottomLeftModel.reparentTo(bottom_piece)
        bottomLeftModel.setPos(0, 0, -0.05)

        bottomMiddleModel.setScale(0.05)
        bottomMiddleModel.reparentTo(bottom_piece)
        bottomMiddleModel.setPos(0.05, 0, -0.05)

        # The Bottom Middle repetitions
        for i in range(1, width+1):
            self.bottom_middle_copy = bottomMiddleModel.copyTo(bottom_piece)
            self.bottom_middle_copy.setPos((0.05*i), 0, -0.05)

        # self.selectableDynamicFrame.ls()
        bottomRightModel.setScale(0.05)
        bottomRightModel.reparentTo(bottom_piece)
        bottomRightModel.setPos((width+1)*0.05, 0, -0.05)

        bottom_piece.flattenStrong()

        return self.selectableDynamicFrame