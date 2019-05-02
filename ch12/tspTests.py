import unittest
from itertools import chain
import datetime
import genetic
import math
import random

def get_fitness(genes, idToLocationLookup):
 fitness = get_distance(idToLocationLookup[genes[0]], idToLocationLookup[genes[-1]])
 for i in range(len(genes) - 1):
  start = idToLocationLookup[genes[i]]
  end = idToLocationLookup[genes[i + 1]]
  fitness += get_distance(start, end)
 return Fitness(round(fitness, 2))

def get_distance(locationA, locationB):
 sideA = locationA[0] - locationB[0]
 sideB = locationA[1] - locationB[1]
 sideC = math.sqrt(sideA * sideA + sideB * sideB)
 return sideC

def display(candidate, startTime):
 timeDiff = datetime.datetime.now() - startTime
 print("{}\t{}\t{}\t{}".format(''.join(map(str, candidate.Genes)), candidate.Fitness, candidate.Strategy.name,timeDiff))

def mutate(genes, fnGetFitness):
 count = random.randint(2, len(genes))
 initialFitness = fnGetFitness(genes) 
 while count > 0:
  count -= 1
  indexA, indexB = random.sample(range(len(genes)), 2)
  genes[indexA], genes[indexB] = genes[indexB], genes[indexA]
  fitness = fnGetFitness(genes)
  if fitness > initialFitness:
   return

def crossover(parentGenes, donorGenes, fnGetFitness):
 pairs = {Pair(donorGenes[0], donorGenes[-1]): 0}
 for i in range(len(donorGenes) - 1):
  pairs[Pair(donorGenes[i], donorGenes[i+1])] = 0
 
 tempGenes = parentGenes[:]
 if Pair(parentGenes[0], parentGenes[-1]) in pairs:
  # find a discontinuity
  found = False
  for i in range(len(parentGenes) - 1):
   if Pair(parentGenes[i], parentGenes[i+1]) in pairs:
    continue
   tempGenes = parentGenes[i+1:] + parentGenes[:i+1]
   found = True
   break
  if not found:
   return None

 runs = [[tempGenes[0]]]
 for i in range(len(tempGenes) - 1):
  if Pair(tempGenes[i], tempGenes[i+1]) in pairs:
   runs[-1].append(tempGenes[i+1])
   continue
  runs.append([tempGenes[i+1]])

 initialFitness = fnGetFitness(parentGenes)
 count = random.randint(2, 20)
 runIndexes = range(len(runs))
 while count > 0:
  count -= 1
  for i in runIndexes:
   if len(runs[i]) == 1:
    continue
   if random.randint(0, len(runs)) == 0:
    runs[i] = [n for n in reversed(runs[i])]
  
  indexA, indexB = random.sample(runIndexes, 2)
  runs[indexA], runs[indexB] = runs[indexB], runs[indexA]
  # flatten
  childGenes = list(chain.from_iterable(runs))
  if fnGetFitness(childGenes) > initialFitness:
   return childGenes
 return childGenes

class Pair: 
 def __init__(self, node, adjacent):
  if node < adjacent:
   node, adjacent = adjacent, node
  self.Node = node
  self.Adjacent = adjacent

 def __eq__(self, other):
  return self.Node == other.Node and self.Adjacent == other.Adjacent

 def __hash__(self):
  return hash(self.Node) * 397 ^ hash(self.Adjacent)

class Fitness:
 def __init__(self, totalDistance):
  self.TotalDistance = totalDistance

 def __gt__(self, other):
  return self.TotalDistance < other.TotalDistance

 def __str__(self):
  return "{:0.2f}".format(self.TotalDistance)

class TravelingSalesmanTests(unittest.TestCase):
 def test_8_queens(self):
  idToLocationLookup = {
   'A':[4, 7],
   'B':[2, 6],
   'C':[0, 5],
   'D':[1, 3],
   'E':[3, 0],
   'F':[5, 1],
   'G':[7, 2],
   'H':[6, 4]
  }
  optimalSequence = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  self.solve(idToLocationLookup, optimalSequence)

 def test_ulysses16(self):
  idToLocationLookup = load_data("ulysses16.tsp")
  optimalSequence = [14, 13, 12, 16, 1, 3, 2, 4, 8, 15, 5, 11, 9, 10, 7, 6]
  self.solve(idToLocationLookup, optimalSequence)

 def solve(self, idToLocationLookup, optimalSequence):
  geneset = [i for i in idToLocationLookup.keys()]

  def fnCreate():
   return random.sample(geneset, len(geneset))

  def fnDisplay(candidate):
   display(candidate, startTime)

  def fnGetFitness(genes):
   return get_fitness(genes, idToLocationLookup)
 
  def fnMutate(genes):
   mutate(genes, fnGetFitness)

  def fnCrossover(parent, donor):
   return crossover(parent, donor, fnGetFitness)

  optimalFitness = fnGetFitness(optimalSequence)
  startTime = datetime.datetime.now()
  best = genetic.get_best(fnGetFitness, None, optimalFitness, None, fnDisplay, fnMutate, fnCreate, maxAge=500, poolSize=25, crossover=fnCrossover) 
  self.assertTrue(not optimalFitness > best.Fitness)

def load_data(localFileName):
 """expects:
   HEADER section before DATA section, all lines start in column 0
   DATA section element all have space in column 0
     <space>1 23.45 67.89
   last line of file is : " EOF"
 """
 with open(localFileName, mode='r') as infile:
  content = infile.read().splitlines()
 idToLocationLookup = {}
 for row in content:
  if row[0] != ' ': # HEADERS
   continue
  if row == " EOF":
   break

  id, x, y = row.split(' ')[1:4]
  idToLocationLookup[int(id)] = [float(x), float(y)]
 return idToLocationLookup


if __name__=="__main__":
 unittest.main()
