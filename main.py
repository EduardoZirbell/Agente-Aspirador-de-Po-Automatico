import numpy as np
import matplotlib.pyplot as plt
import random


TAMANHO = 6  # tamanho da sala

def criar_ambiente():
    ambiente = np.zeros((TAMANHO, TAMANHO))
    
    # visual
    ambiente[0, :] = 1
    ambiente[:, 0] = 1
    ambiente[-1, :] = 1
    ambiente[:, -1] = 1
    
    # adicionar sujeira aleatória 
    for _ in range(TAMANHO):
        x, y = random.randint(1, TAMANHO-2), random.randint(1, TAMANHO-2)
        ambiente[x, y] = 2
    
    return ambiente

def exibir(matriz, posicao):
    plt.imshow(matriz, cmap='nipy_spectral')
    plt.plot([posicao[1]], [posicao[0]], marker='o', color='r', ls='')
    plt.show(block=False)
    plt.pause(0.5)
    plt.clf()

def encontrar_sujeira_mais_proxima(sala, pos):
    sujeiras = np.argwhere(sala == 2)
    if len(sujeiras) == 0:
        return pos
    return min(sujeiras, key=lambda p: abs(p[0] - pos[0]) + abs(p[1] - pos[1]))
  #sinceremante, não sei pq funciona, mas funciona. Deus abençoe o curso em vídeo
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