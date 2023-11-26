from scipy import special as sc
import random
# Constants, experiment parameters
POPULATION_SIZE = 10 #Numero de individuos utilizados ao longo das gerações
MIXING_NUMBER = 2 # Numero de pontos de cruzamento
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

    for row in range(len(rota)-1): #Inicializa o loop baseado no tamanho da rota 
        cidadeAtual = rota[row]
        proximaCidade = rota[row+1]

        if cidadeAtual in cidades and proximaCidade in cidades[cidadeAtual]:
            distanciaTotal += cidades[cidadeAtual][proximaCidade] #Adiciona valor da distancia
        else:
            return "Rota inválida"

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
        if random.randrange(int(sc.comb(POPULATION_SIZE, 2)*2.8)) < fitness_score(MAPA_CIDADES,population[i]):
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


rota_aleatoria_gerada = generate_population("Contagem", "Raposos")


for i in range(len(rota_aleatoria_gerada)):
    print(f"Rota {i+1}")
    print(rota_aleatoria_gerada[i]) 
    distancia_total_exemplo = fitness_score(MAPA_CIDADES, rota_aleatoria_gerada[i])
    print(f"A distância total da rota é: {distancia_total_exemplo}\n")









rota_select = selection(rota_aleatoria_gerada)
cross = crossover(rota_select)

for i in range(len(rota_select)):
    print(f"Rota {i+1}")
    print(rota_select[i]) 
    print(cross[i]) 
    distancia_total_exemplo = fitness_score(MAPA_CIDADES, rota_select[i])
    print(f"A distância total da rota é: {distancia_total_exemplo}\n")
    print(f"A distância total da rota cross é: {fitness_score(MAPA_CIDADES, cross[i])}\n")

 











