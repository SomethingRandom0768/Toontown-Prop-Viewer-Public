
from . import Playground
from dna import DNAStorage, DNAParser
from direct.directnotify import DirectNotifyGlobal

class Cartoonival(Playground.Playground):
    notify = DirectNotifyGlobal.directNotify.newCategory("Cartoonival")
    notify.setDebug(1)

    def __init__(self)-> object:
        ''' Generates Cartoonival
        '''
        super().__init__()

        # Going to use this for placement
        yPosition = 0
        
        # Base DNA Files
        self.loadDNA('phase_6/dna/storage_TF.xml').store(self.dnaStore)

        renderbit = self.loadDNA('phase_6/dna/toonfest_sz.xml').generate(self.dnaStore)

        self.streetGeom = render.attachNewNode(renderbit)
        self.streetGeom.setPos(0, yPosition, 0)

        self.notify.debug("Safezone generated")

    def cleanup(self):
        self.streetGeom.removeNode()