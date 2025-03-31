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
        x, y = np.random.randint(1, tamanho - 1), np.random.randint(1, tamanho - 1)
        # Verifica se a posição já não contém sujeira
        if ambiente[x, y] != 2:
            ambiente[x, y] = 2
    return ambiente


def exibir(matriz, posicao):
    plt.imshow(matriz, cmap="nipy_spectral")
    plt.plot([posicao[1]], [posicao[0]], marker="o", color="r", ls="")
    plt.show(block=False)
    plt.pause(1)
    plt.clf()


def funcaoMapear(posicao, direcao):
    x, y = posicao

    if direcao == "direita":
        if y < 4:  # Move para a direita se não estiver na borda
            return (x, y + 1), "direita"
        elif x < 4:  # Move para baixo ao atingir a borda direita
            return (x + 1, y), "esquerda"
    elif direcao == "esquerda":
        if y > 1:  # Move para a esquerda se não estiver na borda
            return (x, y - 1), "esquerda"
        elif x < 4:  # Move para baixo ao atingir a borda esquerda
            return (x + 1, y), "direita"
    elif direcao == "subindo":
        if y < 4:  # Move para a direita enquanto sobe
            return (x, y + 1), "subindo"
        elif x > 1:  # Move para cima ao atingir a borda direita
            return (x - 1, y), "descendo"
    elif direcao == "descendo":
        if y > 1:  # Move para a esquerda enquanto desce
            return (x, y - 1), "descendo"
        elif x > 1:  # Move para cima ao atingir a borda esquerda
            return (x - 1, y), "subindo"

    return posicao, direcao  # Retorna a mesma posição se não houver movimento possível


def agenteReativoSimples(percepcao):
    posicao, status = percepcao
    chegou_ao_limite = False  # Inicializa o estado de chegada ao limite

    if status == "sujo":
        return "aspirar"  # Aspira se a célula estiver suja

    # Verifica se chegou ao fundo ou ao topo
    if posicao[0] == 4 and posicao[1] == 1 and not chegou_ao_limite:
        chegou_ao_limite = True  # Marca que chegou ao fundo
        direcao = "subindo"  # Altera a direção para subir

    # Mapeia a próxima posição e direção
    nova_posicao, nova_direcao = funcaoMapear(posicao, direcao)

    # Determina a ação com base na nova posição
    if nova_posicao[0] > posicao[0]:
        return "abaixo"
    elif nova_posicao[0] < posicao[0]:
        return "acima"
    elif nova_posicao[1] > posicao[1]:
        return "direita"
    elif nova_posicao[1] < posicao[1]:
        return "esquerda"
    return "parado"  # Caso não haja movimento possível (não esperado)


def ambiente_limpo(ambiente):
    # Verifica se não há mais sujeira no ambiente
    return not np.any(
        ambiente == 2
    )  # Retorna True se não houver células com valor 2 (sujeira)


def simular_agente():
    ambiente = criar_ambiente()
    tamanho = ambiente.shape[0]
    print(tamanho)
    # Define uma posição inicial aleatória dentro do ambiente (não nas paredes)
    posicao = (np.random.randint(1, tamanho - 1), np.random.randint(1, tamanho - 1))

    while not ambiente_limpo(ambiente):  # Continua enquanto houver sujeira no ambiente
        status = "sujo" if ambiente[posicao] == 2 else "limpo"
        acao = agenteReativoSimples((posicao, status))
        nova_posicao = posicao  # Inicializa a nova posição como a atual
        if acao == "aspirar":
            ambiente[posicao] = 0  # Limpa a célula
        elif acao == "acima" and posicao[0] > 1:
            nova_posicao = (posicao[0] - 1, posicao[1])
        elif acao == "abaixo" and posicao[0] < tamanho - 2:
            nova_posicao = (posicao[0] + 1, posicao[1])
        elif acao == "esquerda" and posicao[1] > 1:
            nova_posicao = (posicao[0], posicao[1] - 1)
        elif acao == "direita" and posicao[1] < tamanho - 2:
            nova_posicao = (posicao[0], posicao[1] + 1)

        # Atualiza a posição do agente
        posicao = nova_posicao
        exibir(ambiente, posicao)

    # Exibe o ambiente limpo ao final
    plt.imshow(ambiente, cmap="nipy_spectral")
    plt.title("Ambiente Limpo")
    plt.show()


# Executa a simulação
simular_agente()
