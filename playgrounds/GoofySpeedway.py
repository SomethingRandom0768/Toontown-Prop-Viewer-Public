
from playgrounds import Playground
from dna import DNAStorage, DNAParser
from direct.directnotify import DirectNotifyGlobal

class GoofySpeedway(Playground.Playground):
    notify = DirectNotifyGlobal.directNotify.newCategory("GoofySpeedway")
    notify.setDebug(1)

    def __init__(self, isHoliday=0) -> object:
        '''isHoliday - 1 for Winter, 2 for Halloween
        '''
        super().__init__()

        # Going to use this for placement
        yPosition = 0
        
        # Base DNA Files
        self.loadDNA('phase_6/dna/storage_GS.xml').store(self.dnaStore)
        self.loadDNA('phase_6/dna/storage_GS_sz.xml').store(self.dnaStore)
        self.loadDNA('phase_5/dna/storage_TT_town.xml').store(self.dnaStore)

        # Holiday DNA Files
        if isHoliday == 1:
            self.loadDNA('phase_6/dna/crashed_leaderboard_storage_GS.xml').store(self.dnaStore)
        elif isHoliday == 2:
            self.loadDNA('phase_6/dna/halloween_props_storage_GS.xml').store(self.dnaStore)
        else:
            pass
        
        renderbit = self.loadDNA('phase_6/dna/goofy_speedway_sz.xml').generate(self.dnaStore)
        self.streetGeom = render.attachNewNode(renderbit)
        self.streetGeom.setPos(0, yPosition, 0)
        self.notify.debug("Safezone Generated")

    def cleanup(self):
        self.streetGeom.removeNode()
