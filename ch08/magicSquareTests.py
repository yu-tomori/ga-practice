import unittest
import genetic
import datetime
import random
import numpy as np

def get_fitness(genes):
 squareSize = len(genes)
 fitness = 0
 # それぞれの行の合計値から異形の理論値を引いて絶対値をとったやつの合計値
 for i in range(squareSize):
  fitness += abs((squareSize**2 * (squareSize**2 + 1) / 6)  - sum(genes[i]))
  sumOfVerticalLine = 0
  # それぞれの列の合計値から1行の理論値を引いて絶対値をとったやつの合計値
  for j in range(squareSize):
   sumOfVerticalLine += genes[j][i]
  fitness += abs((squareSize**2 * (squareSize**2 + 1) / 6) - sumOfVerticalLine)
 # 2本の対角線のそれぞれの合計値を理論値でひいて絶対値をとったやつの合計値
 sumOfSouthEastLine = 0
 sumOfNorthEastLine = 0
 for i, j in zip(range(squareSize), range(squareSize)):
  sumOfSouthEastLine += genes[i][j]
  sumOfNorthEastLine += genes[i][squareSize-1-j]
 fitness += abs((squareSize**2 * (squareSize**2 + 1) / 6) - sumOfSouthEastLine)
 fitness += abs((squareSize**2 * (squareSize**2 + 1) / 6) - sumOfNorthEastLine)
 return Fitness(fitness)

def display(candidate, startTime):
 timeDiff = datetime.datetime.now() - startTime
 board = Board(candidate, len(candidate.Genes))
 board.print()
 # print_genes = " " + ''.join(candidate.Genes[i])+ "\n" for i in range(len(candidate))
 print("{}\t{}\t{}".format(candidate.Genes,
  candidate.Fitness,
  timeDiff                            
 )) 

def create(squareSize):
 genes = []
 genes = random.sample(range(1, squareSize**2 + 1), squareSize**2)
 genes = list(np.array_split(genes, squareSize))
 genes = np.array(genes)
 genes = genes.tolist()
 return genes

def mutate(genes, squareSize):
 randomNumOfMutate = 1 # if random.randrange(1, 11) > 1 else 2 
 while randomNumOfMutate > 0:
  randomNumOfMutate -= 1
  indexA, indexB = random.choices(list(range(squareSize)), k=2)
  indexC, indexD = random.choices(list(range(squareSize)), k=2)
  num = genes[indexA][indexB]
  genes[indexA][indexB] = genes[indexC][indexD]
  genes[indexC][indexD] = num

class Fitness:
 def __init__(self, fitness):
  self.fitness = fitness

 def __gt__(self, other):
  return self.fitness < other.fitness

 def __str__(self):
  return "fitness: {}".format(str(self.fitness))

class Board:
 def __init__(self, genes, squareSize):
  self.genes = genes.Genes
  self.squareSize = squareSize

 def print(self):
  for i in reversed(range(len(self.genes))):
   print(i, " ", "".join(map(str, self.genes[i])))

 
class MagicSquareTests(unittest.TestCase):
 def test_3(self):
  self.squareSize = 3
  self.magic_square(self.squareSize)

 def magic_square(self, squareSize):
  startTime = datetime.datetime.now()
 
  def fnDisplay(candidate):
   display(candidate, startTime)

  def fnGetFitness(genes):
   return get_fitness(genes)

  def fnMutate(genes):
   mutate(genes, squareSize)
 
  def fnCreate():
   return create(self.squareSize)

  optimalFitness = Fitness(0)
  best = genetic.get_best(fnGetFitness, squareSize, optimalFitness, None, fnDisplay, custom_mutate=fnMutate, custom_create=fnCreate)
  self.assertTrue(not optimalFitness > best.Fitness)
if __name__ == "__main__":
 unittest.main()
