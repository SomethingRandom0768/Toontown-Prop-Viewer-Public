from direct.gui.DirectSlider import *
from direct.gui.DirectLabel import *
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import DISABLED
from direct.task import *
from .OptionsGUI import OptionsGUI, dynamicFrameGUI
import json

class MusicPlayer(OptionsGUI):
        '''A class that generates a GUI that plays audio'''
        def __init__(self, audioTrackPath, audioName, audioColor):
            '''
            audioTrackPath - path to file
            audioName - name displayed on text
            audioColor - tuple that gives the color
            '''
            super().__init__()

            self.audio = loader.loadSfx(audioTrackPath)
            # self.audio.play()
            self.audioLength = self.audio.length()
            self.audioSlider = DirectSlider(
                text=audioName,
                text_font=self.labelFont,
                text_fg = audioColor,
                text_scale=0.15,
                pos=(0,0,-0.75),
                text_pos=(0,0.1,0),
                range = (0, self.audioLength),
                command = self.setAudioTime,
                thumb_frameSize=(0,0.05,-0.05,0.05),
                geom=self.optionsGeom.find('**/ttr_t_gui_gen_buttons_lineSkinny'),
                geom_scale=(0.51,0.25,0.25)
            )
            self.audioTimeLabel = DirectLabel(
                text='0:00',
                parent=self.audioSlider,
                pos=(-1, 0, -0.15),
                text_font=self.labelFont,
                text_fg = (0.304688, 0.96875, 0.402344, 1.0),
                text_scale=0.1,
                relief=None
            )
            
            self.currentTime = 0
            self.audioSlider.accept('space', self.restartAudio) # Testing
            taskMgr.doMethodLater(1, self.updateText, 'updatingtext')

        def convertTimeToString(self):
            '''Returns a string representation of the current audio time.'''
            convertedMinutes = int(self.currentTime / 60)
            convertedSeconds = self.currentTime % 60
            if convertedSeconds < 9:
                convertedSeconds = str("0") + str( round(convertedSeconds, 0 ) )
            else:
                convertedSeconds = str( round(convertedSeconds, 0) )

            return str(convertedMinutes) + ":" + convertedSeconds

        def setAudioTime(self):
            '''Sets the time of the audio. Useful for checking specific areas of music.'''
            self.currentTime = self.audioSlider['value']
            if self.currentTime == self.audioLength:
                taskMgr.remove('updatingtext')
                self.audio.stop()
            else:                    
                self.audioTimeLabel['text'] = self.convertTimeToString()
                self.audio.setTime(self.currentTime)

        def updateText(self, task):
            '''Task that updates the time and moves the slider to the right each second.'''
            self.currentTime+=1
            self.audioTimeLabel['text'] = self.convertTimeToString()
            self.audioSlider['value'] += 1
            
            return task.again

        def restartAudio(self):
            '''A function that resets the timer. Useful for rewinding back'''
            self.currentTime = 0 # Set the original time to 0
            self.audioSlider['value'] = 0
            self.audioTimeLabel['text'] = '0:00'
            self.audio.play()
            taskMgr.doMethodLater(1, self.updateText, 'updatingtext')   

        def unload(self):
            self.audioSlider.destroy()

        


