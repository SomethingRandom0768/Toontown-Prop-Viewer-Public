
from . import Playground
from dna import DNAStorage, DNAParser
from direct.directnotify import DirectNotifyGlobal

STREET_NUMBERS = {
  1100:  'Barnacle Boulevard',
  1200: 'Seaweed Street',
  1300: 'Lighthouse Lane',
}


class DonaldsDock(Playground.Playground):
    notify = DirectNotifyGlobal.directNotify.newCategory("DonaldsDock")
    notify.setDebug(1)

    def __init__(self, streetNum=0, isHoliday=0) -> object:
        '''isWinter - is it winter?
           streetNum - What street is it?
        '''
        super().__init__()
        # Going to use this for placement
        yPosition = 0

        # Base DNA Files
        self.loadDNA('phase_6/dna/storage_DD.xml').store(self.dnaStore)
        self.loadDNA('phase_6/dna/storage_DD_sz.xml').store(self.dnaStore)
        self.loadDNA('phase_6/dna/storage_DD_town.xml').store(self.dnaStore)

        # Holiday DNA Files
        if isHoliday == 1:
            self.loadDNA('phase_6/dna/winter_storage_DD.xml').store(self.dnaStore)
        elif isHoliday == 2:
            self.loadDNA('phase_6/dna/halloween_props_storage_DD.xml').store(self.dnaStore)
        else:
            pass
    
        # Street DNA Files
        if streetNum:
            renderbit = self.loadDNA('phase_6/dna/donalds_dock_' + str(streetNum) + '.xml').generate(self.dnaStore)
            yPosition = 500
            self.notify.debug(f"Successfully loaded up {STREET_NUMBERS[streetNum]}" )
        else:
            renderbit = self.loadDNA('phase_6/dna/donalds_dock_sz.xml').generate(self.dnaStore)
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
