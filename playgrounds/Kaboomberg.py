
from . import Playground
from dna import DNAStorage, DNAParser
from direct.directnotify import DirectNotifyGlobal

class Kaboomberg(Playground.Playground):
    notify = DirectNotifyGlobal.directNotify.newCategory("Kaboomberg")
    notify.setDebug(1)

    def __init__(self)-> object:
        ''' Generates Kaboomberg
        '''
        super().__init__()

        # Going to use this for placement
        yPosition = 0
        
        # Base DNA Files
        self.loadDNA('phase_8/dna/storage_DG.xml').store(self.dnaStore)
        self.loadDNA('phase_14/dna/storage_DG_kaboomberg.xml').store(self.dnaStore)
        self.loadDNA('phase_14/dna/storage_DG_kaboomberg_sz.xml').store(self.dnaStore)

        renderbit = self.loadDNA('phase_14/dna/daisys_garden_kaboomberg_sz.xml').generate(self.dnaStore)
        self.sky = loader.loadModel('phase_8/models/props/ttr_m_ara_dga_takeOverSkybox.bam')
        self.sky.reparentTo(render)

        self.streetGeom = render.attachNewNode(renderbit)
        self.streetGeom.setPos(0, yPosition, 0)

        self.notify.debug("Safezone Generated")

    def cleanup(self):
        self.streetGeom.removeNode()
        self.sky.removeNode()
