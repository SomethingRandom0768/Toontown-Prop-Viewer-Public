
from . import Playground
from dna import DNAStorage, DNAParser
from direct.directnotify import DirectNotifyGlobal


class ChipAndDales(Playground.Playground):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChipAndDales")
    notify.setDebug(1)

    def __init__(self, golfZoneOrOutdoorZone=0, isHoliday=0) -> object:
        '''isWinter - is it winter?
           streetNum - What street is it?
        '''
        super().__init__()
        # Going to use this for placement
        yPosition = 0
        
        # Base DNA Files
        if golfZoneOrOutdoorZone == 0:
            self.loadDNA('phase_6/dna/storage_OZ.xml').store(self.dnaStore)
            self.loadDNA('phase_6/dna/storage_OZ_sz.xml').store(self.dnaStore)
        else:
            self.loadDNA('phase_6/dna/storage_GZ.xml').store(self.dnaStore)
            self.loadDNA('phase_6/dna/storage_GZ_sz.xml').store(self.dnaStore)

        # Holiday DNA Files
        if isHoliday == 1:
            self.loadDNA('phase_6/dna/halloween_props_storage_OZ.xml').store(self.dnaStore)
        else:
            pass
        
        if golfZoneOrOutdoorZone == 0:
            renderbit = self.loadDNA('phase_6/dna/outdoor_zone_sz.xml').generate(self.dnaStore)
            self.notify.debug("Outdoor Zone generated")
        else:
            renderbit = self.loadDNA('phase_6/dna/golf_zone_sz.xml').generate(self.dnaStore)
            self.notify.debug("Golf Zone generated")

        self.streetGeom = render.attachNewNode(renderbit)
        self.streetGeom.setPos(0, yPosition, 0)

    def cleanup(self):
        self.streetGeom.removeNode()