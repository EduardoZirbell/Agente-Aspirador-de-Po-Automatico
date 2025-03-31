import numpy as np
import matplotlib.pyplot as plt


def criar_ambiente():
    global tamanho
    tamanho = 8
    ambiente = np.zeros((tamanho, tamanho))

    ambiente[0, :] = 1
    ambiente[:, 0] = 1
    ambiente[-1, :] = 1
    ambiente[:, -1] = 1

    area_disponivel = (tamanho - 2) ** 2
    porcentagem_sujeira = 0.75
    num_sujeiras = int(area_disponivel * porcentagem_sujeira)
    
    while np.sum(ambiente == 2) < num_sujeiras:
        x, y = np.random.randint(1, tamanho - 1), np.random.randint(1, tamanho - 1)
        if ambiente[x, y] != 2:
            ambiente[x, y] = 2
    return ambiente

def exibir(matriz, posicao):
    plt.imshow(matriz, cmap="nipy_spectral")
    plt.plot([posicao[1]], [posicao[0]], marker="o", color="r", ls="")
    plt.show(block=False)
    plt.pause(1)
    plt.clf()

def funcaoMapear(posicao, caminhoReverso):
    x, y = posicao
    if not caminhoReverso:
        if x % 2 == 1:
            if y < tamanho - 2:  
                return 'direita', caminhoReverso
            elif x < tamanho - 2: 
                return 'abaixo', caminhoReverso
        else:  
            if y > 1:  
                return 'esquerda', caminhoReverso
            elif x < tamanho - 2:  
                return 'abaixo', caminhoReverso
    else:
        if x % 2 == 1:
            if y > 1:  
                return 'esquerda', caminhoReverso
            elif x > 1: 
                return 'acima', caminhoReverso
        else:  
            if y < tamanho - 2:  
                return 'direita', caminhoReverso
            elif x > 1:  
                return 'acima', caminhoReverso
    return 'parado', caminhoReverso  


def agenteReativoSimples(percepcao, caminhoReverso):
    posicao, status = percepcao
    
    if status == 'sujo':
        return 'aspirar', caminhoReverso
    
    return funcaoMapear(posicao, caminhoReverso)

def ambiente_limpo(ambiente):
    return not np.any(ambiente == 2)

def main():
    ambiente = criar_ambiente()
    tamanho = ambiente.shape[0]
    posicao = (np.random.randint(1, tamanho - 1), np.random.randint(1, tamanho - 1))
    # posicao = (1,1)
    nova_pos = posicao
    caminhoReverso = False
    while not ambiente_limpo(ambiente): 
        if tamanho % 2 == 1:
            if posicao[0] == (tamanho - 2) and posicao[1] == (tamanho - 2):
                caminhoReverso = True
        else:
            if posicao[0] == (tamanho - 2) and posicao[1] == (1):
                caminhoReverso = True
        status = "sujo" if ambiente[posicao] == 2 else "limpo"
        acao, caminhoReverso = agenteReativoSimples((posicao, status), caminhoReverso)
        if acao == 'aspirar':
            ambiente[posicao] = 0
        else:
            x, y = posicao
            if acao == 'direita':
                nova_pos = (x, y + 1) 
            elif acao == 'esquerda':
                nova_pos = (x, y - 1)
            elif acao == 'abaixo':
                nova_pos = (x + 1, y)
            elif acao == 'acima':
                nova_pos = (x - 1, y)

        posicao = nova_pos
        exibir(ambiente, posicao)

    plt.imshow(ambiente, cmap="nipy_spectral")
    plt.title("Ambiente Limpo")
    plt.show()

main()

### 
# Pergunta A: A sua solução é extensível para um mundo 3 x 3? E para um mundo 6 x 6? Explique sua resposta.
# Resposta: Sim, O código foi desenvolvido de forma flexível, permitindo a criação do ambiente e o posicionamento do agente em qualquer tamanho de matriz e posição inicial. 
# Portanto, a lógica de movimentação do agente se adapta a diferentes dimensões, tanto 3x3 quanto 6x6, sem necessidade de alterações no código, além do tamanho da matriz na função de criar_ambiente.
###

