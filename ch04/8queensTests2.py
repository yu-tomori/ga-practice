import unittest
import datetime
import genetic


def display(candidate, startTime, size):
 timeDiff = datetime.datetime.now() - startTime
 board = Board(candidate.Genes, size)
 board.print()
 print("{}\t- {}\t{}".format(
  ''.join(map(str, candidate.Genes)),
  candidate.Fitness,
  timeDiff
 ))

def get_fitness(genes, size):
 board = Board(genes, size)
 # set型のオブジェクトを初期化。set型は重複がない。
 rowsWithQueens = set()
 colsWithQueens = set()
 northEastDiagonalsWithQueens = set()
 southEastDiagonalsWithQueens = set()

 for row in range(size):
  for col in range(size):
   if board.get(row, col) == 'Q':
    rowsWithQueens.add(row)
    colsWithQueens.add(col)
    southEastDiagonalsWithQueens.add(size - 1 - row + col)
    northEastDiagonalsWithQueens.add(row + col)
 total = size - len(rowsWithQueens) + size - len(colsWithQueens) + size - len(southEastDiagonalsWithQueens) + size - len(northEastDiagonalsWithQueens)
 return Fitness(total) 
 

class Fitness:

 def __init__(self, total):
  self.Total = total

 # __gt__ means self > other
 def __gt__(self, other):
  return self.Total < other.Total

 def __str__(self):
  return "{}".format(self.Total)


class Board:
 
 def __init__(self, genes, size):
  board = [['.'] * size for _ in range(size)]
  for index in range(0, len(genes), 2):
   row = genes[index]
   column = genes[index + 1]
   board[column][row] = 'Q'
  self._board = board

 def print(self):
  # 0,0 prints in bottom left corner
  for i in reversed(range(len(self._board))):
   print(''.join(self._board[i]))

 def get(self, row, column):
  return self._board[column][row]


class EightQueensTests(unittest.TestCase):

 def test_benchmark(self):
  genetic.Benchmark.run(lambda: self.test(20))

 def test(self, size=8):
  geneset = [i for i in range(size)]
  startTime = datetime.datetime.now()

  def fnDisplay(candidate):
   display(candidate, startTime, size)

  def fnGetFitness(genes):
   return get_fitness(genes, size)

  optimalFitness = Fitness(0)
  best = genetic.get_best(fnGetFitness, 2 * size, optimalFitness, geneset, fnDisplay)
  self.assertTrue(not optimalFitness > best.Fitness)

if __name__ == '__main__':
 unittest.main()
