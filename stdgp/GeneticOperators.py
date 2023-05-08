from .Individual import Individual
from .Node import Node

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-StdGP
#
# Copyright ©2019-2022 J. E. Batista
#


def tournament(rng, population, n):
	'''
	Selects "n" Individuals from the population and return a 
	single Individual.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	candidates = [rng.randint(0,len(population)-1) for i in range(n)]

	print('SELECTED INDIVIDUALS FOR FITNESS TOURNAMENT:')
	for idx in candidates:
		print(str(population[idx]))
		print('Fitness: ', population[idx].fitness)

	print('SELECTED INDIVIDUAL ON FITNESS TOURNAMENT:')
	print(str(population[min(candidates)]))

	return population[min(candidates)]


def double_tournament(rng, population, tournament_size, sp=3, sf=7, switch = False):
	"""
	Selects 'tournament_size' Individuals for the first tournment until selecting
	'sf' individuals if 'switch' is True OR 'sp' inidividuals if 'switch' is False.

	Then, selects 'sp' individuals out of the 'sf' previously selected ones
	OR
	selects 'sf' individuals out of the 'sp' previously selected ones

	From those last Individuals, return the single best Individual

	Parameters:
	population (list): A list of Individuals
	n: size of first tournament selection
	sp: size of parsimony selection
	sf: size of fitness selection
	"""

	# TODO report: we can say that we decided to recycle the previous tournament function
	# It is easy to order the population by fitness because of the sort method
	# and then call the tournament function with the ordered population, just as what was done before

	# I tjink we can also order the population based on size and then call 'tournament' function
	# with the ordered population, just to be consistent!

	# TODO: see edge cases (sp == sf)

	print('------------ DOUBLE TOURNAMENT SELECTION ------------')

	for ind in population:
		print('Individual: ', str(ind))
		print('Fitness: ', ind.fitness)

	fstournament = []

	if switch:
		if sp >= sf:
			
			# Run the first tournament until selecting 'sp' individuals
			for _ in range(sp):
				# Select 'tournament_size' random Individuals for the first tournament
				candidates = [population[rng.randint(0, len(population) - 1)] for _ in range (tournament_size)]
				
				# Save the best Individual (smalest size) from the first tournament
				fstournament.append(min(candidates, key = lambda x: x.getSize()))
			
			# Order by fitness
			fstournament.sort(reverse = True)

			# Return the best Individual (best fitness) from the second tournament
			return tournament(rng, fstournament, sf)
		else:
			raise Exception('sp must be greater or equal than sf when switch = True')
	else:
		if sf >= sp:
			
			# Sort Individuals by fitness
			population.sort(reverse = True)

			for _ in range(sf):
				# Get the best individual from a first tournament based on fitness and store it
				fstournament.append(tournament(rng, population, tournament_size))
			
			print()
			print('SELECTED INDIVIDUALS IN THE FIRST PHASE OF THE TOURNAMENT:')
			for ind in fstournament:
				print('Individual: ', str(ind))
				print('Fitness : ', ind.fitness)
			
			# Select sp random Individuals from the sf previously selected ones
			# to compete on the second tournament
			candidates = [fstournament[rng.randint(0,len(fstournament) - 1)] for _ in range(sp)]

			print()
			print('SELECTED INDIVIDUALS FOR THE PASIMONY TOURNAMENT:')
			for ind in candidates:
				print(str(ind))
				print('Size: ', ind.getSize())
			
			print()
			print('SELECTED INDIVIDUAL ON PASIMONY TOURNAMENT:')
			print(str(min(candidates, key=lambda x: x.getSize())))

			# Return the Individual with the best size (minimum size)
			return min(candidates, key=lambda x: x.getSize())
		else:
			raise Exception('sf must be greater or equal than sp when switch = False')



def getElite(population,n):
	'''
	Returns the "n" best Individuals in the population.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	return population[:n]


def getOffspring(rng, population, tournament_size, sp, sf, switch):
	'''
	Genetic Operator: Selects a genetic operator and returns a list with the 
	offspring Individuals. The crossover GOs return two Individuals and the
	mutation GO returns one individual. Individuals over the LIMIT_DEPTH are 
	then excluded, making it possible for this method to return an empty list.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	isCross = rng.random()<0.5

	desc = None

	if isCross:
		desc = STXO(rng, population, tournament_size, sp, sf, switch)
	else:
		desc = STMUT(rng, population, tournament_size, sp, sf, switch)

	return desc


def discardDeep(population, limit):
	ret = []
	for ind in population:
		if ind.getDepth() <= limit:
			ret.append(ind)
	return ret


def STXO(rng, population, tournament_size, sp, sf, switch):
	'''
	Randomly selects one node from each of two individuals; swaps the node and
	sub-nodes; and returns the two new Individuals as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''

	print('--------- DOING CROSSOVER --------------')

	ind1 = double_tournament(rng, population, tournament_size, sp, sf, switch)
	ind2 = double_tournament(rng, population, tournament_size, sp, sf, switch)

	h1 = ind1.getHead()
	h2 = ind2.getHead()

	n1 = h1.getRandomNode(rng)
	n2 = h2.getRandomNode(rng)

	n1.swap(n2)

	ret = []
	for h in [h1,h2]:
		i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
		i.copy(h)
		ret.append(i)
	return ret


def STMUT(rng, population, tournament_size, sp, sf, switch):
	'''
	Randomly selects one node from a single individual; swaps the node with a 
	new, node generated using Grow; and returns the new Individual as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = double_tournament(rng, population, tournament_size, sp, sf, switch)
	h1 = ind1.getHead()
	n1 = h1.getRandomNode(rng)
	n = Node()
	n.create(rng, ind1.operators, ind1.terminals, ind1.max_depth)
	n1.swap(n)


	ret = []
	i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
	i.copy(h1)
	ret.append(i)
	return ret
