import genetic
import random
import datetime
import unittest

def generate_parent(length):
 genes = []
 while len(genes) < length:
  sampleSize = min(length - len(genes), len(geneSet))
  genes.extend(random.sample(geneSet, sampleSize))
 return ''.join(genes)

def get_fitness(genes, target):
 return sum(1 for expected, actual in zip(target, genes) if expected == actual)

def mutate(parent):
 index = random.randrange(0, len(parent))
 childGenes = list(parent)
 newGene, alternate = random.sample(geneSet, 2)
 childGenes[index] = alternate if newGene == childGenes[index] else newGene
 return ''.join(childGenes)

def display(candidate, startTime):
 timeDiff = datetime.datetime.now() - startTime
 print("{}\t{}\t{}".format(''.join(candidate.Genes), candidate.Fitness, timeDiff))


# when the unittest module's main function is called, it automatically executes each function whose name starts with test.
class GuessPasswordTests(unittest.TestCase):
 geneset = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"

 
 def test_Hello_World(self):
  target = "Hello World!"
  self.guess_password(target)

 def test_For_I_am_fearfully_and_wonderfully_made(self):
  target = "For I am fearfully and wonderfully made."
  self.guess_password(target)

 def guess_password(self, target):
  startTime = datetime.datetime.now()

  def fnGetFitness(genes):
   return get_fitness(genes, target)
 
  def fnDisplay(candidate): 
   display(candidate, startTime)

  optimalFitness = len(target)
  best =  genetic.get_best(fnGetFitness, len(target), optimalFitness, self.geneset, fnDisplay)
 
  self.assertEqual(''.join(best.Genes), target)

 def test_Random(self):
  length = 150
  target = ''.join(random.choice(self.geneset) for _ in range(length))
  self.guess_password(target)

 """
 def test_benchmark(self):
  genetic.Benchmark.run(self.test_Random)
 """

 def test_onemax(self):
  target = "1" * 100
  self.geneset = '01'
  self.guess_password(target)

if __name__ == '__main__':
 unittest.main()


