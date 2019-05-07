repeatMetas = {'?', '*', '+'}
startMetas = {'|'}
allMetas = repeatMetas | startMetas

import unittest
import re

class RegexTests(unittest.TestCase):
	def test_two_digits(self):
		wanted = {"01", "11", "10"}
		unwanted = {"00", ""}
		self.find_regex(wanted, unwanted, 7)

	def find_regex(self, wanted, unwanted, expectedLength):
		def fnGetFitness(genes):
			return get_fitness(genes, wanted, unwanted)

def get_fitness(genes, wanted, unwanted):
	pattern = ''.join(genes)
	length = len(pattern)

	try:
		re.compile(pattern)
	except re.error:
		return Fitness(0, len(wanted), len(unwanted), length)

	numWantedMatched = sum(1 for i in wanted if re.fullmatch(pattern, i))
	numUnwantedMatched = sum(1 for i in unwanted if re.fullmatch(pattern, i))
	return Fitness(numWantedMatched, len(wanted), numUnwantedMatched, length)

class Fitness:
	def __init__(self, numWantedMatched, totalWanted, numUnwantedMatched, length):
		self.NumWantedMatched = numWantedMatched
		self._totalWanted = totalWanted
		self.NumUnwantedMatched = numUnwantedMatched
		self.Length = length

	def __gt__(self, other):
		combined = (self._totalWanted - self.NumWantedMatched) \
				+ self.NumUnwantedMatched
		otherCombined = (other._totalWanted - other.NumWantedMatched) \
				+ other.NumUnwantedMatched
		if combined != otherCombined:
			return combined < otherCombined

		success = combined == 0
		otherSuccess = otherCombined == 0
		if success != otherSuccess:
			return success
		if not success:
			return False
		
		return self.Length < other.Length

	def __str__(self):
		return "matches: {} wanted, {} unwanted, len {}".format(
				"all" if self._totalWanted == self.NumWantedMatched else self.NumWantedMatched,
				self.NumUnwantedMatched,
				self.Length)
