import numpy as np
import random

soma = 15
tamanho_populacao = 10
geracoes = 5
individuo = [[],
             [],
             []]

def printar_populacao(populacao):
    for i, square in enumerate(populacao):
        print('Square ' + str(i+1) + ': \n' + str(square) + '\n')

def somar_square(square):
    linhas = []
    colunas = []

    diag = np.sum(square.diagonal())
    diag_op = np.sum(square[::-1, :].diagonal())
    diagonais = [diag, diag_op]

    for i in range(0, 3):
        linhas.append(np.sum(square[i, :]))
        colunas.append(np.sum(square[:, i]))

    return linhas, colunas, diagonais

def gerar_populacao(tamanho):
    squares = []

    for numero in range(tamanho):
        # Gerando sequencia aleatoria de 9 digitos
        solucao = random.sample(range(1, 10), 9)
        print("Solução: " + str(solucao))

        square = []

        for i in range(0, 9, 3):
            linha = solucao[i:i+3]
            square.append(linha)
            print("Linha " + str(i) + ": " + str(linha))
            print("Square: " + str(square))
        
        square = np.array(square)
        print("Square " + str(numero+1) + " NumPy:\n" + str(square) + "\n")

        squares.append(square)

    return squares

def fitness(square):
    linhas, colunas, diagonais = somar_square(square)
    
    count = 0

    for sum in linhas, colunas, diagonais:
        if (sum == 15):
            count+=1
            print(count)

    return count

def fix_square(square):
    numeros = list(range(1, 10))

    for i in range (3):
        for j in range(3):
            if square[i][j] in numeros:
                numeros.remove(square[i][j])
            else:
                square[i][j] = numeros.pop()

    return square

def cross_over(fst_parent, snd_parent):
    fst_children = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]
    
    snd_children = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]
    # Ponto de corte
    ponto_corte = random.randint(0, 8) # Ponto de corte aleatório para cada crossover
    # Gera dois filhos
        # Parte superior
    for i in range(ponto_corte // 3): # Escolhe a linha a partir do ponto de corte
        for j in range(ponto_corte+1):
            fst_children[i][j%3] = fst_parent[i][j%3]
            snd_children[i][j%3] = snd_parent[i][j%3]

        # Parte inferior
    for i in range(ponto_corte // 3, 3):
        for j in range(ponto_corte, 9):
            fst_children[i][j%3] = snd_parent[i][j%3]
            snd_children[i][j%3] = fst_parent[i][j%3]

    # Corrigir números duplicados nos filhos
    fst_children = fix_square(fst_children)
    snd_children = fix_square(snd_children)

    return fst_children, snd_children

def algoritmo_genetico(geracoes, tamanho_populacao):
    # Gerar população de soluções
    populacao = gerar_populacao(tamanho_populacao)
    
    # Gerações
    for geracao in range(geracoes):
        print(':Geração ' + str(geracao) + ':')
        # Classificar população por aptidão descrescente
        populacao = sorted(populacao, key=lambda x: fitness(x))
        nova_populacao = []

        # Cross-over
        for i in range(tamanho_populacao // 2):
            # Escolher 2 solucoes aleatoriamente
                # Escolher as duas melhores com prob de 10%
            fst_parent, snd_parent = [], []
            if (random.random() < 0.1):
                fst_parent = random.choice(populacao[: tamanho_populacao // 2])
                snd_parent = random.choice(populacao[: tamanho_populacao // 2])
            else:
                fst_parent = random.choice(populacao)
                snd_parent = random.choice(populacao)

            # Gera dois filhos
            fst_children, snd_children = cross_over(fst_parent, snd_parent)
            # Adiciona os filhos na nova população
            nova_populacao.extend([fst_children, snd_children])
        
        # Mutação

        populacao = nova_populacao

    # Retornar melhor solucao
    melhor_solucao = max(populacao, key=fitness)
    return melhor_solucao, fitness(melhor_solucao)

############################################# main #############################################

def main():

    tamanho = int(input("Digite o tamanho desejado para a população: "))

    populacao = gerar_populacao(tamanho)
    printar_populacao(populacao)

    square = populacao[0]

    diag = square.diagonal()
    print(diag)

    diag_op = square[::-1, :].diagonal()
    print(diag_op)

    linhas, colunas, diagonais = somar_square(square)

    print('SOMAS =================================')
    print('Linhas: ' + str(linhas) + '\nColunas: ' + str(colunas) + '\nDiagonais: ' + str(diagonais))

    melhor_solucao, aptidao = algoritmo_genetico(10, tamanho)

    print("Melhor solução: " + str(melhor_solucao))
    print("\nAptidao: " + str(aptidao))

if __name__ == "__main__":
    main()