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


def rota_aleatoria1(grafo, cidade_inicial, cidade_final):
    # Verifica se as cidades existem no grafo
    if cidade_inicial not in grafo or cidade_final not in grafo:
        return "Cidades não encontradas no grafo"

    # Inicializa a rota com a cidade inicial
    rota = [cidade_inicial]

    # Enquanto não atingir a cidade final
    while rota[-1] != cidade_final:
        #print("a")
        cidade_atual = rota[-1]

        # Obtém os vizinhos da cidade atual
        vizinhos = list(grafo[cidade_atual].keys())

        # Escolhe aleatoriamente um vizinho
        vizinho_aleatorio = random.choice(vizinhos)
     
        rota.append(vizinho_aleatorio)

    return rota

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
 
rota_aleatoria_gerada = generate_population("Contagem", "Raposos")
print(rota_aleatoria_gerada[0]) 

 
distancia_total_exemplo = fitness_score(MAPA_CIDADES, rota_aleatoria_gerada[0])
print(f"A distância total da rota é: {distancia_total_exemplo}")



 











