
from dna import DNAStorage, DNAParser

class Playground():
    def __init__(self) -> None:
        self.dnaStore = DNAStorage.DNAStorage()
        self.loadDNA('phase_4/dna/storage.xml').store(self.dnaStore)
        self.loadDNA('phase_5/dna/storage_town.xml').store(self.dnaStore)

    def loadDNA(self, filename):
        filename = filename

        with open(filename, 'r') as f:
            tree = DNAParser.parse(f)

        return tree