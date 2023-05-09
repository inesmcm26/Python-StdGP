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

	return population[min(candidates)]


def double_tournament(rng, population, tournament_size, sp = 3, sf = 7, switch = False):
	"""
	Selects 'tournament_size' Individuals for the first tournment until selecting
	'sf' individuals if 'switch' is True OR 'sp' inidividuals if 'switch' is False.

	Then, selects 'sp' individuals out of the 'sf' previously selected ones
	OR
	selects 'sf' individuals out of the 'sp' previously selected ones

	From those last Individuals, return the single best Individual

	Parameters:
	population (list): A list of Individuals
	tournament_size: size of first tournament selection
	sp: size of parsimony selection
	sf: size of fitness selection
	"""

	# Create a list to store the winners of the first tournament
	first_tourn_winners = []

	# First tournament based on size and second based on fitness
	if switch:
		if sp >= sf:

			# Sort Individuals in population by size
			population.sort(key = lambda x: x.getSize())
			
			# Run first tournament with size 'tournament_size'
			# until selecting 'sp' winning individuals
			for _ in range(sp):
				first_tourn_winners.append(tournament(rng, population, tournament_size))

			
			# Order winners by fitness
			first_tourn_winners.sort(reverse = True)

			# Run second tournament with size 'sf' and return the best Individual (best fitness)
			return tournament(rng, first_tourn_winners, sf)
		else:
			raise Exception('sp must be greater or equal than sf when switch = True')
	
	# First tournament based on fitness and second based on size
	else:
		if sf >= sp:
			
			# Sort Individuals in population by fitness
			population.sort(reverse = True)

			# Run the first tournament with size 'tournament_size'
			# until selecting 'sf' winning individuals
			for _ in range(sf):
				first_tourn_winners.append(tournament(rng, population, tournament_size))
			
			# Order winners by size
			first_tourn_winners.sort(key = lambda x: x.getSize())

			# Run second tournament with size 'sp' and return the best Individual (best fitness)
			return tournament(rng, first_tourn_winners, sp)

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
