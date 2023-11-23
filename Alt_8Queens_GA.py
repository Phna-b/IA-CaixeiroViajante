from scipy import special as sc
import random
# Constants, experiment parameters
NUM_QUEENS = 8 #Numero de rainhas
POPULATION_SIZE = 10 #Numero de individuos utilizados ao longo das gerações
MIXING_NUMBER = 2 # Numero de pontos de cruzamento
MUTATION_RATE = 0.05 #Chance de cada filho sofrer mutação (5%)


# Create the initial population (solutions)
def generate_population():
    population = []

    for individual in range(POPULATION_SIZE):
        new = [random.randrange(NUM_QUEENS) for idx in range(NUM_QUEENS)] # Gera um numero aleatorio para cada rainha
        print(new)
        print('----')
        population.append(new)

    return population



#Running the experiment

generation = 0

# Generate Random Population
population = generate_population()
#print_found_goal(population)

# Generations until found the solution
#while not print_found_goal(population):
#    print(f'Generation: {generation}')
#    print_found_goal(population)
#    population = evolution(population)
#    generation += 1


#https://www.youtube.com/watch?v=Trbjlxma_PE
#https://colab.research.google.com/drive/1WWQ6VW_gIA_h_mU5xK9Y4BODcz0f44tL?usp=sharing#scrollTo=G1o2VJlC-mMI