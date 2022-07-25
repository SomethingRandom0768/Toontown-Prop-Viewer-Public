
from . import Playground
from dna import DNAStorage, DNAParser
from direct.directnotify import DirectNotifyGlobal

STREET_NUMBERS = {
  3100:  'Walrus Way',
  3200: 'Sleet Street',
  3300: 'Polar Place',
}

class TheBrrrgh(Playground.Playground):
    notify = DirectNotifyGlobal.directNotify.newCategory("TheBrrrgh")
    notify.setDebug(1)

    def __init__(self, streetNum=0, isHoliday=0) -> object:
        '''isWinter - is it winter?
           streetNum - What street is it?
        '''
        super().__init__()
        self.notify = DirectNotify().newCategory("TheBrrrgh")
        # Going to use this for placement
        yPosition = 0
        
        # Base DNA Files

        self.loadDNA('phase_8/dna/storage_BR.xml').store(self.dnaStore)
        self.loadDNA('phase_8/dna/storage_BR_sz.xml').store(self.dnaStore)
        self.loadDNA('phase_8/dna/storage_BR_town.xml').store(self.dnaStore)

        # Holiday DNA Files
        if isHoliday == 1:
            self.loadDNA('phase_8/dna/winter_storage_BR.xml').store(self.dnaStore)
        elif isHoliday == 2:
            self.loadDNA('phase_8/dna/halloween_props_storage_BR.xml').store(self.dnaStore)
        else:
            pass
        
        # Street DNA Files
        if streetNum:
            renderbit = self.loadDNA('phase_8/dna/the_burrrgh_' + str(streetNum) + '.xml').generate(self.dnaStore)
            yPosition = 500
            self.notify.debug(f"Successfully loaded up {STREET_NUMBERS[streetNum]}" )
        else:
            renderbit = self.loadDNA('phase_8/dna/the_burrrgh_sz.xml').generate(self.dnaStore)
            self.sky = loader.loadModel('phase_3.5/models/props/BR_sky.bam')
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
