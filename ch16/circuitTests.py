import unittest
import random
import datetime
import circuits
import genetic

def get_fitness(genes, rules, inputs):
	circuit = nodes_to_circuit(genes)[0]
	sourceLabels = "ABCD"
	rulesPassed = 0
	# inputs = dict()
	for rule in rules:
		inputs.clear()
		inputs.update(zip(sourceLabels, rule[0]))
		if circuit.get_output() == rule[1]:
			rulesPassed += 1
	return rulesPassed

def nodes_to_circuit(genes):
	circuit = []
	usedIndexes = []
	for i, node in enumerate(genes):
		used = {i}
		inputA = inputB = None
		if node.IndexA is not None and i > node.IndexA:
			inputA = circuit[node.IndexA]
			used.update(usedIndexes[node.IndexA])
			if node.IndexB is not None and i > node.IndexB:
				inputB = circuit[node.IndexB]
				used.update(usedIndexes[node.IndexB])
		circuit.append(node.CreateGate(inputA, inputB))
		usedIndexes.append(used)
	return circuit[-1], usedIndexes[-1]

def create_gene(index, gates, sources):
	if index < len(sources):
		gateType = sources[index]
	else:
		gateType = random.choice(gates)
	indexA = indexB = None
	# Not and And
	if gateType[1].input_count() > 0:
		indexA = random.randint(0, index)
	# And
	if gateType[1].input_count() > 1:
		indexB = random.randint(0, index) if index > 1 and index >= len(sources) else 0
		if indexB == indexA:
			indexB = random.randint(0, index)
	return Node(gateType[0], indexA, indexB)

def mutate(childGenes, fnCreateGene, fnGetFitness, sourceCount):
	count = random.randint(1, 5)
	initialFitness = fnGetFitness(childGenes)
	while count > 0:
		count -=1
		indexesUsed = [i for i in nodes_to_circuit(childGenes)[1] if i >= sourceCount]
		index = random.choice(indexesUsed)
		childGenes[index] = fnCreateGene(index)
		if fnGetFitness(childGenes) > initialFitness:
			return

def display(candidate, startTime):
	circuit = nodes_to_circuit(candidate.Genes)[0]
	timeDiff = datetime.datetime.now() - startTime
	print("{}\t{}\t{}".format(circuit, candidate.Fitness, timeDiff))

class Node:
	def __init__(self, createGate, indexA=None, indexB=None):
		# createGateにはgeneset[.][0]が入る.
		self.CreateGate = createGate
		# Notの時は、indexAのみに値が入る.
		# Sourceの時は、indexに値が入らない.
		self.IndexA = indexA
		self.IndexB = indexB

class CircuitTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.inputs = dict()
		cls.gates = [[circuits.And, circuits.And], [lambda i1, i2: circuits.Not(i1), circuits.Not]]
		cls.sources = [[lambda i1, i2: circuits.Source('B', cls.inputs), circuits.Source],
						[lambda i1, i2: circuits.Source('A', cls.inputs), circuits.Source]]

	def test_generate_0_OR(self):
		rules = [[[False, False], False],
				[[False, True], True],
				[[True, False], True],
				[[True, True], True]]

		optimalLength = 6
		self.find_circuit(rules, optimalLength)

	def test_generate_1_XOR(self):
		rules = [[[False, False], False],
				[[False, True], True],
				[[True, False], True],
				[[True, True], False]]
		optimalLength = 11
		self.find_circuit(rules, optimalLength)

	def test_generate_2_AxBxC(self):
		rules = [[[False, False, False], False],
				[[False, False, True], True],
				[[False, True, False], True],
				[[False, True, True], False],
				[[True, False, False], True],
				[[True, False, True], False],
				[[True, True, False], False],
				[[True, True, True], True]]
		self.sources.append([lambda l, r: circuits.Source('C', self.inputs), circuits.Source])
		self.gates.append([circuits.Or, circuits.Or])
		self.find_circuit(rules, 12)

	def get_2_bit_adder_rules_for_bit(self, bit):
		rules = [[[0,0,0,0], [0,0,0]],
				[[0,0,0,1], [0,0,1]],
				[[0,0,1,0], [0,1,0]],
				[[0,0,1,1], [0,1,1]],
				[[0,1,0,0], [0,0,1]],
				[[0,1,0,1], [0,1,0]],
				[[0,1,1,0], [0,1,1]],
				[[0,1,1,1], [1,0,0]],
				[[1,0,0,0], [0,1,0]],
				[[1,0,0,1], [0,1,1]],
				[[1,0,1,0], [1,0,0]],
				[[1,0,1,1], [1,0,1]],
				[[1,1,0,0], [0,1,1]],
				[[1,1,0,1], [1,0,0]],
				[[1,1,1,0], [1,0,1]],
				[[1,1,1,1], [1,1,0]]]
		bitNRules = [[rule[0], rule[1][2 - bit]] for rule in rules]
		if not [circuits.Xor, circuits.Xor] in self.gates:
			self.gates.append([circuits.Xor, circuits.Xor])
		if not [lambda l, r: circuits.Source('D', self.inputs), circuits.Source] \
				in self.sources:
			self.sources.append([lambda l, r: circuits.Source('D', self.inputs), \
				circuits.Source])
		return bitNRules

	def test_generate_3_2_bit_adder_1s_bit(self):
		rules = self.get_2_bit_adder_rules_for_bit(0)
		self.find_circuit(rules, 3)

	def test_generate_4_2_bit_adder_2s_bit(self):
		rules = self.get_2_bit_adder_rules_for_bit(1)
		self.find_circuit(rules, 7)

	def test_generate_5_2_bit_adder_4s_bit(self):
		rules = self.get_2_bit_adder_rules_for_bit(2)
		self.find_circuit(rules, 9)

	def find_circuit(self, rules, expectedLength):
		startTime = datetime.datetime.now()

		def fnGetFitness(genes):
			return get_fitness(genes, rules, self.inputs)

		def fnDisplay(candidate, length=None):
			if length is not None:
				print("--distinct nodes in circuit:",
				len(nodes_to_circuit(candidate.Genes)[1]))
			display(candidate, startTime)

		def fnCreateGene(index):
			return create_gene(index, self.gates, self.sources)

		def fnMutate(genes):
			mutate(genes, fnCreateGene, fnGetFitness, len(self.sources))

		maxLength = 50

		def fnCreate():
			return [fnCreateGene(i) for i in range(maxLength)]

		def fnOptimizationFunction(variableLength):
			nonlocal maxLength
			maxLength = variableLength
			return genetic.get_best(fnGetFitness, None, len(rules), None, fnDisplay, fnMutate,
								fnCreate, poolSize = 3, maxSeconds=30)

		def fnIsImprovement(currentBest, child):
			return child.Fitness == len(rules) and \
					len(nodes_to_circuit(child.Genes)[1]) < \
					len(nodes_to_circuit(currentBest.Genes)[1])

		def fnIsOptimal(child):
			return child.Fitness == len(rules) and \
					len(nodes_to_circuit(child.Genes)[1]) <= expectedLength

		def fnGetNextFeatureValue(currentBest):
			return len(nodes_to_circuit(currentBest.Genes)[1])

		best = genetic.hill_climbing(fnOptimizationFunction, fnIsImprovement, fnIsOptimal,
									fnGetNextFeatureValue, fnDisplay, maxLength)
		self.assertTrue(best.Fitness == len(rules))
		self.assertFalse(len(nodes_to_circuit(best.Genes)[1]) > expectedLength)
		print("\n")

if __name__ == "__main__":
	unittest.main()
