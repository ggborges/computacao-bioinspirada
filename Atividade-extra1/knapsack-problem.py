import random, time

# Parâmetros do problema
n_itens = 100
w_capacidade = 100
tamanho_populacao = 90
geracoes = 100
iteracoes = 10
itens, populacao = [], []

# Pesos entre [1 ~ 50]
# Lucros entre [1 ~ 1000]

def gerar_populacao():
    # Gerando aleatoriamente 100 itens com pesos entre 1~50 e lucros entre 1~1000
    print("\n-----------\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Gerando itens aleatoriamente\n\n")
    global itens # indica o uso de variável global
    itens = [[random.randint(1, 50), random.randint(1, 1000)] for _ in range(n_itens)]
    
    print(str(itens) + "\n")

    # População é uma lista de 150 listas de tamanho 100 com 0s e 1s [0 para item fora da bolsa, 1 para item dentro da bolsa]
    print("\n------------\n\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\ Gerando população\n\n")
    global populacao
    populacao = [[random.randint(0, 1) for _ in range(n_itens)] for _ in range (tamanho_populacao)]

    print(str(populacao))


def fitness(solucao):
    peso_total, lucro_total, aptidao = 0, 0, 0
    global itens, w_capacidade
    for item in range(len(solucao)):
        if solucao[item] == 1: # item está na mochila
            peso_total += itens[item][0]
            lucro_total += itens[item][1]
    
    penalidade = w_capacidade / peso_total
    penalidade2 = max(0, peso_total - w_capacidade)
    
    aptidao = lucro_total * penalidade - penalidade2

    #print("Aptidão: " + str(aptidao) + "\nLucro total: " + str(lucro_total) + "\nPeso total: " + str(peso_total) + "\n" + "Penalidade: " + str(penalidade) + " / (1/1+penalidade): " + str((1/1+penalidade)) + "\n\n")

    return peso_total, lucro_total, aptidao

def selecao_pais():
    print("!!!!!! Seleção dos pais !!!!!!")
    # Roleta
    global populacao
    pai1, pai2 = [], []
    roleta = []
    fitness_roleta = 0
    probs = {} # Dicionário pra registrar as probabilidades de cada
    
    # Selecionando indivíduos para a roleta+torneio
    for i in range(5):
        selecionado = populacao[random.randint(0, len(populacao) - 1)]
        if selecionado not in roleta:
            roleta.append(selecionado)
            _, _, aptidao = fitness(selecionado)
            # Incrementa fitness total para calcular probabilidades
            fitness_roleta += aptidao
            # Preenchendo o dicionário inicialmente com os valores individuais de aptidao
            probs[f'candidato{len(roleta)-1}'] = aptidao
            print(f'Probs com aptidao:\n{probs}\n')
    
    print('########## $$ mudando de aptidao para probabilidade $$ ##########')
    for index, candidato in enumerate(probs):
        aptidao = probs[candidato]
        prob = (aptidao / fitness_roleta)
        print(f'Candidato: {index} => Aptidao: {aptidao} & Prob: {prob}\n')
        
        if index == 0:
            probs[candidato] = [0, prob] # transformando o valor em probabilidade
            print(f'{probs}\n')
        else:        
            valor_anterior = probs[f'candidato{index-1}'][1]
            probs[candidato] = [valor_anterior, valor_anterior + prob]
            print(f'{probs}\n')
        
    
    pais = []
    
    pais = roleta_torneio(probs, roleta)
    pai1, pai2 = pais[0], pais[1]
    
        
    return pai1, pai2

def roleta_torneio(probs, roleta):
    pais, candidatos = [], []
    
    print('Começou a roleta!\n.\n..\n...\n')
    while len(pais) < 2:
        prob = random.uniform(0, 1)
        print(f'Número sorteado:{prob}')
        for index, candidato in enumerate(probs):
            probi = probs[candidato]
            if probi[0] < prob and prob < probi[1]:
                vencedor = roleta[index]
                if vencedor not in pais:
                    pais.append(vencedor)
                    candidatos.append(candidato)
                    
    print(f'Pais: {pais}\nProb pai1: {probs[candidatos[0]]}\nProb pai2: {probs[candidatos[1]]}\n')
    
    return pais
            
def algoritmo_genetico(qtde_geracoes):
    gerar_populacao()
    global populacao, itens
    nova_populacao = []

    for geracao in range(qtde_geracoes):
        print(f"\n-------------\n¨¨¨¨¨¨¨¨¨¨¨¨¨¨ ~~~~~~~~~~~~~~ Geração {geracao+1} ~~~~~~~~~~~~~~ ¨¨¨¨¨¨¨¨¨¨¨¨¨¨\n\n")
        nova_populacao = []
        
        while len(nova_populacao) != len(populacao):
            pai1, pai2 = selecao_pais()        

            # Recombinação (probabilidade de 75%)
            prob_crossover = 0.75
            if random.random() < prob_crossover:
                ponto_corte = random.randint(0, len(pai1) - 1)
                
                filho1 = pai1[ponto_corte:] + pai2[:ponto_corte]
                filho2 = pai1[:ponto_corte] + pai2[ponto_corte:]
                filhos = [filho1, filho2]
                print(f"Pai1: {pai1}\nPai2: {pai2}\nFilho1: {filho1}\nFilho2: {filho2}\n")
            
                # Mutação
                prob_mutacao = 0.025
                for filho in filhos:
                    if random.random() < prob_mutacao:
                        print("Mutou!\n")
                        # Mutação de mais de um bit
                        for i in filho:
                            if random.random() < 0.5:
                                filho[i] = 1 - filho[i]
                
                nova_populacao.extend(filhos)
            else: # Não recombinou, copia os pais 
                nova_populacao.extend([pai1, pai2])       

        populacao = nova_populacao
        
        # Condição de término
        #melhor_solucao = max(populacao, key=fitness)
        populacao_ordenada = sorted(populacao, key=fitness)
        melhor_solucao = populacao_ordenada[0]
        pior_solucao = populacao_ordenada[len(populacao) - 1]
        peso, lucro, aptidao = fitness(pior_solucao)
        print(f"\n[][][][][][][][][][][][][][][][][][][]\no\nPior solucao: {pior_solucao}\nPeso: {peso}\n Lucro: {lucro}\n Aptidao: {aptidao}\n")
        peso, lucro, aptidao = fitness(melhor_solucao)
        print(f"\n[][][][][][][][][][][][][][][][][][][]\no\nMelhor solucao: {melhor_solucao}\nPeso: {peso}\n Lucro: {lucro}\n Aptidao: {aptidao}\n")
        
        global w_capacidade
        if peso <= w_capacidade:
            break
            # Quantidade máxima de gerações
            # Fitness mínimo (para após alcançar um indíviduo com um fitness aceitável)
                # "Nível mínimo de diversidade" (limite para menor valor de desvio-padrão entre os fitness na população)
                # "Quantidade máxima de gerações sem melhora significativa do fitness"
    
    soma_fitness = 0
    for solucao in populacao:
        _, _, fitness_individuo = fitness(solucao)
        soma_fitness += fitness_individuo
        
    media_fitness = soma_fitness / tamanho_populacao    
    
    return media_fitness, aptidao, peso

def main():
    #gerar_populacao()
    #selecao_pais()
    execution_times_list, time_minutes_list, medias_fitness, melhores_fitness, pesos_finais = [], [], [], [], []
    begin = time.time()
    for _ in range(iteracoes):
        start = time.time()
        media_fitness, melhor_fitness, peso_melhor_fitness = algoritmo_genetico(geracoes)
        end = time.time()
        
        execution_time = end - start
        time_minutes = execution_time / 60
        
        print(f"\n====================\n--------------\n...........\n.....\n...\nTempo de execução: {execution_time} ms\nTempo em minutos: {execution_time / 60} minutos\n...\n.....\n............\nMédia Fitness: {media_fitness}\n")
        
        execution_times_list.append(execution_time)
        time_minutes_list.append(time_minutes)
        medias_fitness.append(media_fitness)
        melhores_fitness.append(melhor_fitness)
        pesos_finais.append(peso_melhor_fitness)
    #for i in range(len(populacao)):
    #    fitness(populacao[i])
    finish = time.time()
    print(f"\n\nOOOOOOOOOOOOOOOOooooooo Infos oooooooOOOOOOOOOOOOOOOO\n\n")
    print(f"Tempos de execução: {execution_times_list}\n-- Em minutos: {time_minutes_list}\nMedias de fitness: {medias_fitness}\nMelhores Fitness: {melhores_fitness}\n")
    tempo_iteracoes = finish - begin
    print(f"\n********* Tempo total **********\n\n{tempo_iteracoes/60} min\n{(tempo_iteracoes / 60) / 60} h\n")
    print(f"Medias fitness: {medias_fitness}\nMelhores fitness: {melhores_fitness}\nPesos das soluções finais: {pesos_finais}")
    
if __name__ == '__main__':
    main()
