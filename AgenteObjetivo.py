import numpy as np
import matplotlib.pyplot as plt

def criar_ambiente():
    # Variável que define o tamanho do ambiente
    tamanho = 6
    # Criação do ambiente com o tamanho definido
    ambiente = np.zeros((tamanho, tamanho))

    # Adicionando paredes ao ambiente
    # Valor : é utilizado para alterar o valor da coluna ou linha por completo
    ambiente[0, :] = 1
    ambiente[:, 0] = 1
    # Valor -1 é utilizado para representar a última linha ou coluna da matriz
    ambiente[-1, :] = 1
    ambiente[:, -1] = 1
    
    # Calcula a área disponível para sujeira
    area_disponivel = (tamanho - 2) ** 2 
    # Define a porcentagem de sujeira (75%)
    porcentagem_sujeira = 0.75
    # Calcula o número de sujeiras a serem adicionadas
    num_sujeiras = int(area_disponivel * porcentagem_sujeira)
    
    # Repete o loop até que a quantidade de sujeiras seja atingida
    while np.sum(ambiente == 2) < num_sujeiras:
        # Gera coordenadas aleatórias para a sujeira
        x, y = np.random.randint(1, tamanho-1), np.random.randint(1, tamanho-1)
        # Verifica se a posição já não contém sujeira
        if ambiente[x, y] != 2:  
            ambiente[x, y] = 2
    return ambiente

def exibir(matriz, posicao):
    plt.imshow(matriz, cmap='nipy_spectral')
    plt.plot([posicao[1]], [posicao[0]], marker='o', color='r', ls='')
    plt.show(block=False)
    plt.pause(1)
    plt.clf()

def encontrar_sujeira_mais_proxima(sala, pos):
    sujeiras = np.argwhere(sala == 2)
    
    if len(sujeiras) == 0:
        return pos
    
    print(min(sujeiras, key=lambda p: abs(p[0] - pos[0]) + abs(p[1] - pos[1])))
    return min(sujeiras, key=lambda p: abs(p[0] - pos[0]) + abs(p[1] - pos[1]))

def agenteObjetivo(sala):
    pos = (1, 1)
    pontos = 0
    while checkObj(sala):
        percepcao = sala[pos]
        if percepcao == 2:
            sala[pos] = 0
            acao = 'aspirar'
        else:
            nova_pos = encontrar_sujeira_mais_proxima(sala, pos)
            if nova_pos[0] > pos[0]:
                pos = (pos[0] + 1, pos[1])
            elif nova_pos[0] < pos[0]:
                pos = (pos[0] - 1, pos[1])
            elif nova_pos[1] > pos[1]:
                pos = (pos[0], pos[1] + 1)
            elif nova_pos[1] < pos[1]:
                pos = (pos[0], pos[1] - 1)
            acao = 'mover'
        pontos += 1
        print(f"Estado da percepcao: {percepcao} Acao escolhida: {acao}")
        exibir(sala, pos)
    print(f"Pontos: -> {pontos}")
    
    # visualizar a parada
    plt.imshow(sala, cmap='nipy_spectral')
    plt.plot([pos[1]], [pos[0]], marker='o', color='r', ls='')
    plt.show()

def checkObj(sala):
    return 1 if 2 in sala else 0

environment = criar_ambiente()
agenteObjetivo(environment)