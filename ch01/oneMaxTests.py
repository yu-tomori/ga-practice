import unittest
import datetime
import genetic

def get_fitness(genes):
 # return a count the number of 1's in the genes
 return genes.count(1)

def display(candidate, startTime):
 # display the current genes, their fitness, and elapsed time
 timeDiff = datetime.datetime.now() - startTime
 print("{}\t{}\t{}".format(
  ''.join(map(str, candidate.Genes)), 
  candidate.Fitness, 
  timeDiff
 ))

class OneMaxTests(unittest.TestCase):

 
 def test(self, length=100):

  geneset = [0, 1]
  startTime = datetime.datetime.now()
  # create the helper function and optimal fitness
  def fnDisplay(candidate):
   display(candidate, startTime)

  def fnGetFitness(genes):
   return get_fitness(genes)

  optimalFitness = length
  # then call 'genetic'.get_best()
  best_genes = genetic.get_best(fnGetFitness, length, optimalFitness, geneset, fnDisplay)
  # finally, assert that the fitness of the result is optimal
  self.assertEqual(best_genes.Fitness, optimalFitness)

 def test_benchmark(self):
  genetic.Benchmark.run(lambda: self.test(4000))

if __name__ == '__main__':
 unittest.main()
