
from . import Playground
from dna import DNAStorage, DNAParser
from src import OptionsGUI
from direct.directnotify import DirectNotifyGlobal

STREET_NUMBERS = {
  2100:  'Silly Street',
  2200: 'Loopy Lane',
  2300: 'Punchline Place',
}

class ToontownCentral(Playground.Playground):
    notify = DirectNotifyGlobal.directNotify.newCategory("ToontownCentral")
    notify.setDebug(1)
    
    def __init__(self, streetNum=0, isHoliday=0) -> object:
        '''isHoliday - 1 for Winter, 2 for Halloween
           streetNum - Street Zone ID?
        '''
        super().__init__()

        # Going to use this for placement
        yPosition = 0
        
        # Base DNA Files
        self.loadDNA('phase_4/dna/storage_TT.xml').store(self.dnaStore)
        self.loadDNA('phase_4/dna/storage_TT_sz.xml').store(self.dnaStore)
        self.loadDNA('phase_5/dna/storage_TT_town.xml').store(self.dnaStore)
        
        # Holiday DNA Files
        if isHoliday == 1:
            self.loadDNA('phase_4/dna/winter_storage_TT.xml').store(self.dnaStore)
            self.loadDNA('phase_4/dna/winter_storage_TT_sz.xml').store(self.dnaStore)
        elif isHoliday == 2:
            self.loadDNA('phase_4/dna/halloween_props_storage_TT.xml').store(self.dnaStore)
            self.loadDNA('phase_4/dna/halloween_props_storage_TT_sz.xml').store(self.dnaStore)
        else:
            pass
        
        # Street DNA Files
        if streetNum:
            renderbit = self.loadDNA('phase_5/dna/toontown_central_' + str(streetNum) + '.xml').generate(self.dnaStore)
            yPosition = 500
            self.notify.debug(f"Successfully loaded up {STREET_NUMBERS[streetNum]}" )
        else:
            renderbit = self.loadDNA('phase_4/dna/toontown_central_sz.xml').generate(self.dnaStore)
            self.sky = loader.loadModel('phase_3.5/models/props/TT_sky.bam')
            self.sky.reparentTo(render)
            self.notify.debug("Safezone generated")

        self.streetGeom = render.attachNewNode(renderbit)
        self.streetGeom.setPos(0, yPosition, 0)


    def cleanup(self):
        self.streetGeom.removeNode()
        del self.streetGeom
        try:
            self.sky.removeNode()
            del self.sky
        except:
            pass
