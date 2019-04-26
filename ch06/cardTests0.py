import unittest
import datetime
import genetic

def display(candidate, startTime):
 timeDiff = datetime.datetime.now() - startTime
 print("{}\t{}\t{}".format(' '.join(map(str, candidate.Genes)), candidate.Fitness, timeDiff))

def get_fitness(genes):
 fitness = 0

 for i in range(1, 11):
  if genes.count(i) != 1:
   fitness += -1
 
 first_half = genes[:5]
 last_half = genes[5:]
 product = 1
 sums = 0
 for a in first_half:
  product *= a
 fitness += -1 * abs(360 - product)
 for b in last_half:
  sums += b
 fitness += -1 * abs(36 - sums)
 return fitness

class CardTests(unittest.TestCase):
 geneset = [i for i in range(1, 11)] 

 def test_card(self):
  startTime = datetime.datetime.now()
  def fnDisplay(candidate):
   display(candidate, startTime)

  def fnGetFitness(genes):
   return get_fitness(genes)

  optimalValue = 0
  best = genetic.get_best(fnGetFitness, 10, optimalValue, self.geneset, fnDisplay)
  self.assertTrue(oprimalValue == best.Fitness)


if __name__ == "__main__":
 unittest.main()
