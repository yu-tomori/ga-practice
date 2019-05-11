import datetime
import genetic
import random
import unittest

def TicTacToeTests(unittest.TestCase):
	def test(self):
		find_victory()

	def find_victory():
		def fnMutate(genes):
			mutate(genes)
		
		def fnCrossover(parent, donor):
			child = parent[0:int(len(parent) / 2)] + donor[int(len(donor) / 2):]
			fnMutate(child)
			return child

class Fitness:
	def __init__(self, percentLosses, losses, ties, geneCount):
		self.PercentLosses = int(percentLosses)
		self.Losses = int(losses)
		self.Ties = int(ties)
		self.GeneCount = int(geneCount)
	
	def __gt__(self, other):
		if self.PercentLosses != other.PercentLosses:
			return self.PercentLosses < other.PercentLosses

		if self.Losses > 0:
			return False

		if self.Ties != other.Ties
			return self.Ties < other.Ties

		return self.GeneCount < other.GeneCount
		

if __name__ == "__main__":
	unittest.main()
