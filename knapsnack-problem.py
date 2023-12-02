import random

# Parâmetros do problema da mochila

itens = [(2, 40), (5, 30), (10, 50), (5, 10), (4, 20), (8, 15), (3, 18), (12, 55)] # (peso, valor)
capacidade_mochila = 16
num_geracoes = 100
tamanho_populacao = 100

# Função de aptidão

def aptidao(solucao):
    peso_total = 0
    valor_total = 0

    for i in range(len(solucao)):
        if solucao[i] == 1:
            peso_total += itens[i][0]
            valor_total += itens[i][1]

            # Se o peso total da solucao exceder a capacidade da mochila
            # penaliza a solucao
            if peso_total > capacidade_mochila:
                return 0
    
    return valor_total

# Algoritmo genético

def algoritmo_genetico(num_geracoes, tamanho_populacao):
    # Gerando população, lista de listas
    #       Lista com 100 listas de 0s e 1s (item dentro ou não da mochila)
    populacao = [[random.randint(0, 1) for _ in range(len(itens))] for _ in range(tamanho_populacao)]

    # Criando gerações
    for geracao in range(num_geracoes):
        # Classificar por aptidão descrescente
        populacao = sorted(populacao, key=lambda x: -aptidao(x))
        nova_populacao = []

        # Cross-over (cruzamento)
        for i in range(len(populacao) // 2):
            # Escolhe duas solucoes aleatoriamente na primeira metade da populacao
            # Dessa forma garante que serão escolhidas solucoes de maiores aptidoes
            fst_parent = random.choice(populacao[: tamanho_populacao // 2])
            snd_parent = random.choice(populacao[: tamanho_populacao // 2])
            
            # Divide a solucao em alguma lugar aleatório
            ponto_corte = random.randint(0, len(itens) - 1)

            # Gera dois filhos com combinações diferentes dos pais
            fst_children = fst_parent[:ponto_corte] + snd_parent[ponto_corte:]
            snd_children = fst_parent[ponto_corte:] + snd_parent[:ponto_corte]
            # Adiciona os filhos da nova_populacao
            nova_populacao.extend([fst_children, snd_children])
            
            # nova_populacao.append(fst_children)
            # nova_populacao.append(snd_children)

        # Mutação
        prob_mutacao = 0.1

        for i in range(len(nova_populacao)):
            if random.random() < prob_mutacao:
                # Mutação de apenas um bit
                bit_mutacao = random.randint(0, len(itens) - 1)
                nova_populacao[i][bit_mutacao] = 1 - nova_populacao[i][bit_mutacao]
                
                # Mutacao de mais de um bit
                for j in range(len(itens)):
                    if random.random() < 0.5:
                        nova_populacao[i][j] = 1 - nova_populacao[i][j]

        populacao = nova_populacao
    
    melhor_solucao = max(populacao, key=aptidao)
    return melhor_solucao, aptidao(melhor_solucao)


def main():

    melhor_solucao, melhor_valor = algoritmo_genetico(100, 100)
    print("Melhor solução encontrada: ", melhor_solucao)
    print("Melhor valor: ", melhor_valor)

if __name__ == "__main__":
    main()