from scipy import special as sc
import random
# Constants, experiment parameters
POPULATION_SIZE = 30 #Numero de individuos utilizados ao longo das gerações
MIXING_NUMBER = 4 # Numero de pontos de cruzamento
MUTATION_RATE = 0.05 #Chance de cada filho sofrer mutação (5%)
MAPA_CIDADES = {
    "Belo Horizonte": {"Contagem": 21, "Nova Lima": 23, "Sabara": 18, "Brumadinho": 56, "Santa Luzia": 27},
    "Contagem": {"Belo Horizonte": 21, "Betim": 17},
    "Betim": {"Contagem": 17, "Mario Campos": 18},
    "Mario Campos": {"Betim": 18, "Brumadinho": 13},
    "Nova Lima": {"Belo Horizonte": 23, "Raposos": 8, "Sabara": 16, "Brumadinho": 62},
    "Sabara": {"Belo Horizonte": 18, "Nova Lima": 16, "Raposos": 12, "Santa Luzia": 24, "Lagoa Santa": 50},
    "Raposos": {"Nova Lima": 16, "Sabara": 12},
    "Brumadinho": {"Belo Horizonte": 56, "Mario Campos": 13, "Nova Lima": 62},
    "Santa Luzia": {"Belo Horizonte": 27, "Lagoa Santa": 26, "Sabara": 24},
    "Lagoa Santa": {"Santa Luzia": 26, "Sabara": 50}
}


# Create the initial population (solutions)
def generate_population(cidadeInicial):
    population = []
    for individual in range(POPULATION_SIZE):
        population.append(rota_aleatoria_volta_origem(MAPA_CIDADES, cidadeInicial))
    return population

def fitness_score(cidades, rota):
    distanciaTotal = 0
    for row in range(len(rota)-1): #Inicializa o loop baseado no tamanho da rota 
        cidadeAtual = rota[row]
        proximaCidade = rota[row+1]

        if cidadeAtual in cidades and proximaCidade in cidades[cidadeAtual]:
            distanciaTotal += cidades[cidadeAtual][proximaCidade] #Adiciona valor da distancia
        else:
            return 100000

    return distanciaTotal



import random

def rota_aleatoria_volta_origem(grafo, cidade_inicial):
    # Verifica se a cidade inicial existe no grafo
    if cidade_inicial not in grafo:
        return "Cidade inicial não encontrada no grafo"

    # Inicializa a rota com a cidade inicial
    rota = [cidade_inicial]

    # Enquanto não atingir a cidade inicial novamente
    x = 0
    while x < (len(MAPA_CIDADES)):
        cidade_atual = rota[-1]

        # Obtém os vizinhos da cidade atual que ainda não foram visitados
        vizinhos_nao_visitados = [vizinho for vizinho in grafo[cidade_atual] if vizinho not in rota]

        # Se não houver mais vizinhos disponíveis, volta à cidade inicial
        if not vizinhos_nao_visitados:
            rota.append(cidade_inicial)
        else:
            # Escolhe aleatoriamente um vizinho não visitado
            vizinho_aleatorio = random.choice(vizinhos_nao_visitados)
            rota.append(vizinho_aleatorio)
        x = x+1
    return rota

 

 


def selection(population):
    parents = []
    i = 0
    for ind in population:
        #select parents with probability proportional to their fitness score
        
        if random.randrange(int(sc.comb(POPULATION_SIZE, 2)*2.0)) < fitness_score(MAPA_CIDADES,population[i]) and  fitness_score(MAPA_CIDADES,population[i]) < 100000 :
            parents.append(ind)
        i = i+1

    return parents


import itertools
def crossover(parents):

    #random indexes to to cross states with
    cross_points = random.sample(range(POPULATION_SIZE), MIXING_NUMBER - 1)
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
            if type(parent_part) is not int:
                offspring.append(parent_part)

            #update index pointer
            start_pt = cross_point

        #last parent
        last_parent = perm[-1]
        parent_part = last_parent[cross_point:]
        if type(parent_part) is not int:
            offspring.append(parent_part)

        #flatten the list since append works kinda differently
        if type(parent_part) is not int:
            offsprings.append(list(itertools.chain(*offspring)))
 
        offsprings = [value for value in offsprings if type(value) != int]
    return offsprings


def mutate(seq):
    for row in range(len(seq)):
        if random.random() < MUTATION_RATE:
            rand1 =  random.randrange(1,len(seq[row])-1)
            cidadeAlt =str(seq[row][rand1])
            cidadeAnterior = str(seq[row][rand1-1])
            cidadePosterior = str(seq[row][rand1+1])
            possibilidadeEntrada = [vizinho for vizinho in MAPA_CIDADES[cidadeAnterior] if vizinho not in cidadeAlt]  
            escolha_aleatoria = random.choice(possibilidadeEntrada)
            if cidadePosterior in MAPA_CIDADES[escolha_aleatoria]:
                print("PASSEI")
                print("ROTA ANTIGA")
                print(seq[row])
                seq[row][rand1] = escolha_aleatoria
                print(seq[row])
                return seq

    return seq

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

    new_gen = sorted(new_gen, key=lambda ind: fitness_score(MAPA_CIDADES,ind), reverse=True)[:POPULATION_SIZE]

    return new_gen


# Print the solution
def print_found_goal(population, to_print=True):
    for ind in population:
        score = fitness_score(MAPA_CIDADES,ind)
        if to_print:
            print(f'{ind}. Score: {score}')
        if score == sc.comb(POPULATION_SIZE, 2):
            if to_print:
                print('Solution found')
            return True

    if to_print:
        print('Solution not found')
    return False



rota_aleatoria_gerada = generate_population("Belo Horizonte")


#for i in range(len(rota_aleatoria_gerada)):
#    print(f"Rota {i+1}")
#    print(rota_aleatoria_gerada[i])
#    distancia_total_exemplo = fitness_score(MAPA_CIDADES, rota_aleatoria_gerada[i])
#    print(f"A distância total da rota é: {distancia_total_exemplo}\n")


cros = selection(rota_aleatoria_gerada)
cros = crossover(rota_aleatoria_gerada)


for i in range(len(cros)):
    print(f"Rota - Cross {i+1}")
    print(cros[i])
    distancia_total_exemplo = fitness_score(MAPA_CIDADES, cros[i])
    print(f"A distância total da rota é: {distancia_total_exemplo}\n")

mutate(rota_aleatoria_gerada)
 
 
 




 











