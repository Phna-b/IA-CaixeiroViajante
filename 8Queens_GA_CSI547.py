from scipy import special as sc
# Constants, experiment parameters
NUM_QUEENS = 8 #Numero de rainhas
POPULATION_SIZE = 5 #Numero de individuos utilizados ao longo das gerações
MIXING_NUMBER = 2 # Numero de pontos de cruzamento
MUTATION_RATE = 0.05 #Chance de cada filho sofrer mutação (5%)

# Create the fitness score - How good is a solution?
def fitness_score(seq):
    score = 0

    for row in range(NUM_QUEENS):
        col = seq[row]

        for other_row in range(NUM_QUEENS):

            #queens cannot pair with itself
            if other_row == row:
                continue
            if seq[other_row] == col:
                continue
            if other_row + seq[other_row] == row + col:
                continue
            if other_row - seq[other_row] == row - col:
                continue
            #score++ if every pair of queens are non-attacking.
            score += 1

    #divide by 2 as pairs of queens are commutative
    return score/2

# Create the selection operator acording their fitness score
# Select best solutions for next step: crossover
import random
from scipy import special as sc

def selection(population):
    parents = []

    for ind in population:
        #select parents with probability proportional to their fitness score
        if random.randrange(sc.comb(NUM_QUEENS, 2)*2) < fitness_score(ind):
            parents.append(ind)


    return parents

# Create the crossover operator
# Combine features of each solution using a crossover point
import itertools
def crossover(parents):

    #random indexes to to cross states with
    cross_points = random.sample(range(NUM_QUEENS), MIXING_NUMBER - 1)
    offsprings = []

    #all permutations of parents
    permutations = list(itertools.permutations(parents, MIXING_NUMBER))

    for perm in permutations:
        offspring = []

        #track starting index of sublist
        start_pt = 0

        for parent_idx, cross_point in enumerate(cross_points): #doesn't account for last parent

            #sublist of parent to be crossed
            parent_part = perm[parent_idx][start_pt:cross_point]
            offspring.append(parent_part)

            #update index pointer
            start_pt = cross_point

        #last parent
        last_parent = perm[-1]
        parent_part = last_parent[cross_point:]
        offspring.append(parent_part)

        #flatten the list since append works kinda differently
        offsprings.append(list(itertools.chain(*offspring)))

    return offsprings


# Create the routine to mutate a solution
# A operator to create diversity in the population
def mutate(seq):
    for row in range(len(seq)):
        if random.random() < MUTATION_RATE:
            seq[row] = random.randrange(NUM_QUEENS)

    return seq


# Print the solution
def print_found_goal(population, to_print=True):
    for ind in population:
        score = fitness_score(ind)
        if to_print:
            print(f'{ind}. Score: {score}')
        if score == sc.comb(NUM_QUEENS, 2):
            if to_print:
                print('Solution found')
            return True

    if to_print:
        print('Solution not found')
    return False


# Create the routine to implement the evolution
def evolution(population):
    #select individuals to become parents
    parents = selection(population)

    #recombination. Create new offsprings
    offsprings = crossover(parents)

    #mutation
    offsprings = list(map(mutate, offsprings))

    #introduce top-scoring individuals from previous generation and keep top fitness individuals
    new_gen = offsprings

    for ind in population:
        new_gen.append(ind)

    new_gen = sorted(new_gen, key=lambda ind: fitness_score(ind), reverse=True)[:POPULATION_SIZE]

    return new_gen

# Create the initial population (solutions)
def generate_population():
    population = []

    for individual in range(POPULATION_SIZE):
        new = [random.randrange(NUM_QUEENS) for idx in range(NUM_QUEENS)] # Gera um numero aleatorio para cada rainha
        population.append(new)

    return population



#Running the experiment

generation = 0

# Generate Random Population
population = generate_population()
#print_found_goal(population)
offsprings = crossover(population)
list(map(mutate, offsprings))
# Generations until found the solution
print(offsprings)