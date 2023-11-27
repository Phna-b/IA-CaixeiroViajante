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
    "Sabara": {"Belo Horizonte": 18, "Nova Lima": 16, "Raposos": 12, "Santa Luzia": 24, "Santa Luzia": 50},
    "Raposos": {"Nova Lima": 16, "Sabara": 12},
    "Brumadinho": {"Belo Horizonte": 56, "Mario Campos": 13, "Nova Lima": 62},
    "Santa Luzia": {"Belo Horizonte": 27, "Lagoa Santa": 26, "Sabara": 24},
    "Lagoa Santa": {"Santa Luzia": 26, "Sabara": 50}
}


# Create the initial population (solutions)
def generate_population(cidadeInicial, cidadeFinal):
    population = []

    for individual in range(POPULATION_SIZE):
        population.append(rota_aleatoria(MAPA_CIDADES, cidadeInicial, cidadeFinal))
    return population


def fitness_score(cidades, rota):
    distanciaTotal = 0
    if type(rota) is int:
        return 200000
    else:
        for row in range(len(rota)-1): #Inicializa o loop baseado no tamanho da rota 
            cidadeAtual = rota[row]
            proximaCidade = rota[row+1]

            if cidadeAtual in cidades and proximaCidade in cidades[cidadeAtual]:
                distanciaTotal += cidades[cidadeAtual][proximaCidade] #Adiciona valor da distancia
            else:
                return 100000

    return distanciaTotal



def rota_aleatoria(grafo, cidade_inicial, cidade_final):
    # Verifica se as cidades existem no grafo
    if cidade_inicial not in grafo or cidade_final not in grafo:
        return "Cidades não encontradas no grafo"

    # Inicializa a rota com a cidade inicial
    rota = [cidade_inicial]

    # Enquanto não atingir a cidade final
    while rota[-1] != cidade_final:
        cidade_atual = rota[-1]

        # Obtém os vizinhos da cidade atual
        vizinhos = [vizinho for vizinho in grafo[cidade_atual] if vizinho not in rota]

        # Se não houver mais vizinhos disponíveis, retorna a rota
        if not vizinhos:
            rota = rota_aleatoria(grafo, cidade_inicial, cidade_final)
            return rota

        # Escolhe aleatoriamente um vizinho
        vizinho_aleatorio = random.choice(vizinhos)
     
        rota.append(vizinho_aleatorio)

    return rota
 


def selection(population):
    parents = []
    i = 0
    for ind in population:
        #select parents with probability proportional to their fitness score
            
        if random.randrange(int(sc.comb(POPULATION_SIZE, 2)*2.0)) < fitness_score(MAPA_CIDADES,population[i]):
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
            rand1 =  random.randrange(len(seq[row])-1)
            rand2 =  random.randrange(len(seq[row])-1)
            troca = seq[row][rand1]
            seq[row][rand1] = seq[row][rand2]
            seq[row][rand2] = troca
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



rota_aleatoria_gerada = generate_population("Belo Horizonte", "Raposos")


#for i in range(len(rota_aleatoria_gerada)):
#    print(f"Rota {i+1}")
#    print(rota_aleatoria_gerada[i]) 
#    distancia_total_exemplo = fitness_score(MAPA_CIDADES, rota_aleatoria_gerada[i])
#    print(f"A distância total da rota é: {distancia_total_exemplo}\n")


rota_select = selection(rota_aleatoria_gerada)
cross = crossover(rota_select)
mutates = mutate(rota_aleatoria_gerada)
    
for i in range(len(rota_select)):
    print(f"Selecionados - Rota {i+1}")
    print(rota_select[i]) 
    distancia_total_exemplo = fitness_score(MAPA_CIDADES, rota_select[i])
    print(f"A distância total da rota é: {distancia_total_exemplo}\n")
    

for i in range(len(cross)):
    print(f"Crossover - Rota {i+1}")
    print(cross[i]) 
    print(f"A distância total da rota cross é: {fitness_score(MAPA_CIDADES, cross[i])}\n")

#for i in range(len(mutates)):
#    print(f"Crossover Mutante - Rota {i+1}")
#    print(mutates[i]) 
#    print(f"A distância total da rota cross é: {fitness_score(MAPA_CIDADES, mutates[i])}\n")

 
 
 
 




 











