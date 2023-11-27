import random
 

grafo_distancias ={
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

import random

def trocar_posicao_cidades(variavel, cidade1, cidade2):
    if cidade1 not in variavel or cidade2 not in variavel:
        return "Pelo menos uma das cidades não encontrada na variável"

    index_cidade1 = variavel.index(cidade1)
    index_cidade2 = variavel.index(cidade2)

    variavel[index_cidade1], variavel[index_cidade2] = variavel[index_cidade2], variavel[index_cidade1]

    return variavel

# Exemplo de uso
rota_exemplo = ["Belo Horizonte", "Contagem", "Betim", "Nova Lima", "Sabara"]
nova_rota = trocar_posicao_cidades(rota_exemplo, "Contagem", "Nova Lima")

print(f"Rota Original: {rota_exemplo}")
print(f"Nova Rota: {nova_rota}")