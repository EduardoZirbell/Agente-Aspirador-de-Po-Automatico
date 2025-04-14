import numpy as np
import matplotlib.pyplot as plt

def criar_ambiente():
    tamanho = 6
    ambiente = np.zeros((tamanho, tamanho))

    ambiente[0, :] = 1
    ambiente[:, 0] = 1
    ambiente[-1, :] = 1
    ambiente[:, -1] = 1
    
    area_disponivel = (tamanho - 2) ** 2 
    porcentagem_sujeira = 0.50
    num_sujeiras = int(area_disponivel * porcentagem_sujeira)
    
    while np.sum(ambiente == 2) < num_sujeiras:
        x, y = np.random.randint(1, tamanho-1), np.random.randint(1, tamanho-1)
        if ambiente[x, y] != 2:  
            ambiente[x, y] = 2
    return ambiente

def exibir(matriz, posicao):
    plt.imshow(matriz, cmap='nipy_spectral')
    plt.plot([posicao[1]], [posicao[0]], marker='o', color='r', ls='')
    plt.show(block=False)
    plt.pause(0.1)
    plt.clf()

def encontrar_sujeira_mais_proxima(sala, pos):
    sujeiras = np.argwhere(sala == 2)
    
    if len(sujeiras) == 0:
        return pos
    
    distancias = np.abs(sujeiras - pos).sum(axis=1)
    sujeira_mais_proxima = sujeiras[np.argmin(distancias)]
    return tuple(sujeira_mais_proxima)

def agenteObjetivo(percepcao, sala, pos):
    if percepcao == 2:
        return 'aspirar', pos
    else:
        nova_pos = encontrar_sujeira_mais_proxima(sala, pos)
        if nova_pos[0] > pos[0]:
            direcao = 'baixo'
        elif nova_pos[0] < pos[0]:
            direcao = 'cima'
        elif nova_pos[1] > pos[1]:
            direcao = 'direita'
        elif nova_pos[1] < pos[1]:
            direcao = 'esquerda'
        return direcao, nova_pos

def ambiente_limpo(sala):
    return not np.any(sala == 2)

def main():
    ambiente = criar_ambiente()
    posicao = (1, 1)
    pontos = 0

    while not ambiente_limpo(ambiente):
        percepcao = ambiente[posicao]
        acao, nova_pos = agenteObjetivo(percepcao, ambiente, posicao)
        
        if acao == 'aspirar':
            ambiente[posicao] = 0
        else:
            if nova_pos[0] > posicao[0]:
                posicao = (posicao[0] + 1, posicao[1])
            elif nova_pos[0] < posicao[0]:
                posicao = (posicao[0] - 1, posicao[1])
            elif nova_pos[1] > posicao[1]:
                posicao = (posicao[0], posicao[1] + 1)
            elif nova_pos[1] < posicao[1]:
                posicao = (posicao[0], posicao[1] - 1)

        pontos += 1
        print(f"Estado da percepção: {percepcao} | Ação escolhida: {acao}")
        exibir(ambiente, posicao)

    print(f"Pontos: {pontos}")
    plt.imshow(ambiente, cmap='nipy_spectral')
    plt.plot([posicao[1]], [posicao[0]], marker='o', color='r', ls='')
    plt.title("Ambiente Limpo")
    plt.show()

main()