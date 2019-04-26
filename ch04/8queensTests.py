import unittest
import datetime
import genetic
import numpy as np

def get_fitness(genes):
 fitness = 0

 # horizonal
 for i in range(0, 8):
  gene_block = []
  start_index = i * 8
  finish_index = 8 + (i * 8)
  gene_block = genes[start_index:finish_index]
  if gene_block.count(1) == 0:
   fitness += -1
   continue
  fitness += gene_block.count(1) * -1 + 1

 # vertical
 for i in range(0, 8):
  gene_block = []
  gene_block = genes[i::8]
  if gene_block.count(1) == 0:
   fitness += -1
   continue
  fitness += gene_block.count(1) * -1 + 1

 # diagonal \
 for i in range(0, 7):
  gene_block = []
  gene_block = genes[i::9]
  gene_block = gene_block[0:(8 - i)]
  # to prevent from subtracting 1 when a diagonal line have one "1".
  if gene_block.count(1) == 0: 
   continue
  fitness += gene_block.count(1) * -1 + 1
 
 # diagonal \'
 for i in [8,16,24,32,40,48]:
  gene_block = []
  gene_block = genes[i::9]
  gene_block = gene_block[0:(8 - (i // 8))]
  if gene_block.count(1) == 0:
   continue
  fitness += gene_block.count(1) * -1 + 1

 # diagonal /
 for i in range(1, 8):
  gene_block = []
  gene_block = genes[i::7]
  gene_block = gene_block[0:(i + 1)]
  if gene_block.count(1) == 0:
   continue
  fitness += gene_block.count(1) * -1 +1

 # diagonal /'
 for i in [15, 23, 31, 39, 47, 55]:
  gene_block = []
  gene_block = genes[i::7]
  gene_block = gene_block[0:( 9-((i+1)//8) )]
  if gene_block.count(1) == 0:
   continue
  fitness += gene_block.count(1) * -1 + 1

 return fitness

def display(candidate, startTime):
 timeDiff = datetime.datetime.now() - startTime
 fitness = candidate.Fitness
 candidate = np.array(candidate.Genes)
 candidate = np.split(candidate, 8)
 print("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\t{}".format(
  candidate[0],
  candidate[1],
  candidate[2], 
  candidate[3],
  candidate[4],
  candidate[5],
  candidate[6],
  candidate[7],
  fitness, 
  timeDiff
 ))

class EightQueensTests(unittest.TestCase):

 def test_8_queens(self):
  self.deploy_queens(64)

 def deploy_queens(self, totalNumbers):
  geneset = [0, 1]
  startTime = datetime.datetime.now()
  
  def fnDisplay(candidate):
   display(candidate, startTime)
 
  def fnGetFitness(genes):
   return get_fitness(genes)

  optimalFitness = 0
  best = genetic.get_best(fnGetFitness, totalNumbers, optimalFitness, geneset, fnDisplay)
  self.assertTrue(best.Fitness == 0)

if __name__ == '__main__':
 unittest.main()
 

