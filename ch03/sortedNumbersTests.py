import unittest
import datetime
import genetic

def get_fitness(genes):
 fitness = 1
 gap = 0
 
 for i in range(1, len(genes)):
  if genes[i] > genes[i - 1]:
   fitness += 1
  else:
   gap += genes[i - 1] - genes[i]
 return Fitness(fitness, gap)

def display(candidate, startTime):
 timeDiff = datetime.datetime.now() - startTime
 sorted_numbers = ', '.join(map(str, candidate.Genes))
 print("{}\t{}\t{}".format(sorted_numbers, candidate.Fitness, timeDiff))

class Fitness:

 def __init__(self, numbersInSequenceCount, totalGap):
  self.NumbersInSequenceCount = numbersInSequenceCount
  self.TotalGap = totalGap
 
 def __gt__(self, other):
  if self.NumbersInSequenceCount != other.NumbersInSequenceCount:
   return self.NumbersInSequenceCount > other.NumbersInSequenceCount
  return self.TotalGap < other.TotalGap

 def __str__(self):
  return "{} Sequential, {} Total Gap".format(self.NumbersInSequenceCount, self.TotalGap)

class SourtedNumbersTests(unittest.TestCase):
 
 def test_sort_3_numbers(self):
  self.sort_numbers(3)

 def test_sort_10_numbers(self):
  self.sort_numbers(10)
 
 def test_benchmark(self):
  genetic.Benchmark.run(lambda: self.sort_numbers(40))

 def sort_numbers(self, totalNumbers):
  geneset = [i for i in range(100)]
  startTime = datetime.datetime.now()
  def fnGetFitness(genes):
   return get_fitness(genes)

  def fnDisplay(candidate):
   display(candidate, startTime)

  optimalFitness = Fitness(totalNumbers, 0)
  best = genetic.get_best(fnGetFitness, totalNumbers, optimalFitness, geneset, fnDisplay)
  self.assertTrue(not optimalFitness > best.Fitness)

if __name__ == '__main__':
 unittest.main()

