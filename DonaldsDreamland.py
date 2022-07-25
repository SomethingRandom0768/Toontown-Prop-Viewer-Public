
from . import Playground
from dna import DNAStorage, DNAParser
from direct.directnotify import DirectNotifyGlobal

STREET_NUMBERS = {
  9100:  'Lullaby Lane',
  9200: 'Pajama Place',
}

class DonaldsDreamland(Playground.Playground):
    notify = DirectNotifyGlobal.directNotify.newCategory("DonaldsDreamland")
    notify.setDebug(1) 

    def __init__(self, streetNum=0, isHoliday=0) -> object:
        '''isWinter - is it winter?
           streetNum - What street is it?
        '''
        super().__init__()
        # Going to use this for placement
        yPosition = 0
        
        # Base DNA Files
        self.loadDNA('phase_8/dna/storage_DL.xml').store(self.dnaStore)
        self.loadDNA('phase_8/dna/storage_DL_sz.xml').store(self.dnaStore)
        self.loadDNA('phase_8/dna/storage_DL_town.xml').store(self.dnaStore)

        # Holiday DNA Files
        if isHoliday == 1:
            self.loadDNA('phase_8/dna/winter_storage_DL.xml').store(self.dnaStore)
        elif isHoliday == 2:
            self.loadDNA('phase_8/dna/halloween_props_storage_DL.xml').store(self.dnaStore)
        else:
            pass
        
        # Street DNA Files
        if streetNum:
            renderbit = self.loadDNA('phase_8/dna/donalds_dreamland_' + str(streetNum) + '.xml').generate(self.dnaStore)
            yPosition = 500
            self.notify.debug(f"Successfully loaded up {STREET_NUMBERS[streetNum]}" )
        else:
            renderbit = self.loadDNA('phase_8/dna/donalds_dreamland_sz.xml').generate(self.dnaStore)
            self.sky = loader.loadModel('phase_8/models/props/DL_sky.bam')
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