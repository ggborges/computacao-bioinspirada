###############################
"""
. Representação: permutação de string de bits
    ex: [000, 001, 010, 011, 100, 101, 110, 111]
        [ 0 ,  1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ]
        [ r1,  r2,  r3,  r4,  r5,  r6,  r7,  r8]
        
. Inicialização: aleatória

. Número de filhos gerados: 2 (dois)
"""
###############################
import random, time, sys
from itertools import permutations
from typing import List


Solucao = List[str]
Populacao = List[Solucao]

tamanho_populacao = 100
geracoes = 100
prob_recombinacao = 0.9
prob_mutacao = 0.4
posicoes = ["000", "001", "010", "011", "100", "101", "110", "111"]
populacao = []
#populacao_ordenada = []
fitnesses = []
fitness_medio_ger = []
#fitnesses_ordenado = []
count_fitness = 0


def gerar_populacao():
    print("\n---------------------------\n..::Gerar população::..")
    global tamanho_populacao, populacao, fitnesses
    
    populacao = []
    
    for _ in range(tamanho_populacao):
        visitados, solucao = [], []
        for i in enumerate(posicoes):
            done = False
            while not done:
                rand_index = random.randint(0, len(posicoes)-1)
                if posicoes[rand_index] not in visitados:
                    solucao.append(posicoes[rand_index])
                    visitados.append(posicoes[rand_index])
                    done = True                    
        print(solucao)
        print(visitados)
        populacao.append(solucao)
        print("Solução adicionada à população.")
    
    fitnesses = fitness_grupo(populacao)
    pares = list(zip(fitnesses, populacao))
    pares_ordenados = sorted(pares, key=lambda x: x[0])
    fitnesses = [par[0] for par in pares_ordenados]
    populacao = [par[1] for par in pares_ordenados]
    
def check_position(position: str):
    real_position = 0
    for index, char in enumerate(position):
        real_position += int(char) * (2**(2-index))
    
    return real_position
        
def fitness(solucao: Solucao):
    #print("\n---------------------------\n..::Fitness:..")
    global count_fitness
    count_fitness += 1
    #print("$$$$$$$$$ ######### CONTAGEM ######### $$$$$$$$$")
    #print(f"Contagem de Fitness: {count_fitness}\n\n")
    choques = 0
    for i, posicao in enumerate(solucao):
        position = check_position(posicao)
        
        for j in range(len(solucao)):
            if j != i:
                diff_w = abs(i - j)
                diff_h = abs(position - check_position(solucao[j]))
                if diff_w == diff_h:
                    choques += 1
            #print("fitness em desenvolvimento")
    
    return choques // 2
    
def fitness_grupo(population: Populacao):
    print("\n---------------------------\n..::fitness_grupo()::..")
    # Gera o fitness de cada indivíduo da populacao
    global fitnesses
    fitnesses_grupo = []
    for solucao in population:
        fitnesses_grupo.append(fitness(solucao))
    
    if len(population) == len(populacao):
        fitnesses = fitnesses_grupo
        
    return fitnesses_grupo

def selecao_pais():
    print("\n---------------------------\n..::Seleção de pais::..")
    global populacao, fitnesses
    pai1, pai2, roleta = [], [], []
    pares = list(zip(fitnesses, populacao))
    # Escolher 5 indivíduos aleatoriamente com igual probabilidade
    while len(roleta) < 5:
        i_random = random.randint(0, len(populacao)-1)
        escolhido = pares[i_random]
        if escolhido not in roleta:
            roleta.append(escolhido)
            
    pai1, pai2 = roleta_torneio(roleta)
        
    return pai1, pai2

def roleta_torneio(roleta: List[List[str]]):
    print("\n---------------------------\n..::Roleta::..")
    roleta_ordenada = sorted(roleta, key=lambda x: x[0])
    return roleta_ordenada[0][1], roleta_ordenada[1][1]

def mutacao(individuo: List[str]):
    #print("Indivíduo: ", individuo)
    fst_gen = random.randint(0, len(individuo) - 1)
    snd_gen = 0
    done = False
    print("\n---------------------------\n..::Mutação::..")
    #print(f"Solução original:\n - {individuo}\n\n")
    while not done:
        snd_gen = random.randint(0, len(individuo) - 1)
        if(snd_gen != fst_gen):
            done = True
    
    aux = individuo[snd_gen]
    individuo[snd_gen] = individuo[fst_gen]
    individuo[fst_gen] = aux
    #print(". .. ... mutação em andamento ... .. .")
    #print(f"Solução mutante:\n - {individuo}\n\n")
    return individuo

def crossfill(corte_pai, pai: Solucao):
    filho = Solucao
    filho = corte_pai
    #for i in range(len(corte_pai), (len(pai) - len(corte_pai)))
    i = len(corte_pai)
    while len(filho) < 8:
        #print("Pai[i]: ", pai[i])
        #print("Filho: ", filho)
        if pai[i] not in filho: filho.append(pai[i])
        if i < 7: i += 1
        else: i = 0
    
    #print("Filho: ", filho)
    return filho

def crossover(pai1: Solucao, pai2: Solucao):
    filhos = []
    ponto_corte = random.randint(0, len(pai1))
    corte1 = pai1[:ponto_corte]
    corte2 = pai2[:ponto_corte]
    #print(f"Pai1: {pai1}\nPai2: {pai2}\nPonto de corte: {ponto_corte}\n")
    #print(f"Corte do pai 1: {corte1}\nCorte do pai 2: {corte2}\n")
    filho1 = crossfill(corte1, pai2)
    filho2 = crossfill(corte2, pai1)
    filhos = [filho1, filho2]
    
    return filhos

def substituicao_pior(filhos, fitnesses_filhos):
    global populacao, fitnesses
    #print(f"População: {len(populacao)} - Fitnesses: {len(fitnesses)}")
    fitnesses_aux = fitnesses + fitnesses_filhos
    #print("Fitnesses dos filhos: ", fitnesses_filhos)
    populacao_aux = populacao + filhos
    #print(f"Populacao aux: {populacao_aux}\nTamanho pop aux: {len(populacao_aux)}\nFitnesses aux: {fitnesses_aux}\nTamanho fit aux: {len(fitnesses_aux)}\n")
    
    pares = list(zip(fitnesses_aux, populacao_aux))
    pares_ordenados = sorted(pares, key=lambda x: x[0])
    #print(f"Pares: {pares}\n Tamanho pares: {len(pares)}")
    #print(f"Pares ordenados: {pares_ordenados}\n Tamanho pares ordenados: {len(pares_ordenados)}")

    fitnesses_aux = [par[0] for par in pares_ordenados]
    populacao_aux = [par[1] for par in pares_ordenados]
    #print(f"Tamanho fit aux: {len(fitnesses_aux)}")
    #print(f"Tamanho pop aux: {len(populacao_aux)}")
    
    fitnesses = fitnesses_aux[:100]
    populacao = populacao_aux[:100]
    
    #print(f"Tamanho pop: {len(populacao)}")

    #print(f"Fitnesses: {fitnesses}\nTamanho fit: {len(fitnesses)}")
    #print(f"Populacao: {populacao}\nTamanho pop: {len(populacao)}")
    
    global tamanho_populacao
    if len(populacao) == tamanho_populacao:
        print("Ok!") 
    else:         
        str_erro = f"Erro com tamanho da população.\nlen(pop): {len(populacao)} - len(fit): {len(fitnesses)}\n"
        str_objetos = f"População: {populacao}\nFitnesses: {fitnesses}"
        raise TypeError(str_erro+str_objetos)
    
    #print("População: ", len(populacao))
    #print("Fitnesses: ", len(fitnesses))
    #print("População ordenada: ", len(populacao_ordenada))
    #print("Fitnesses ordenado: ", len(fitnesses_ordenado))

def selecao_sobreviventes(filhos):
    print("\n---------------------------\n..::Seleção de sobreviventes::..")
    #print("len(filhos): ", len(filhos))
    #print("Filho1: ", filhos[0])
    #print("Filho2: ", filhos[1])
    fitnesses_filhos = fitness_grupo(filhos)
    #print("Debugando ::Seleção de sobreviventes::")
    #print(f"Filhos: {filhos}\nFitnesses filhos: {fitnesses_filhos}")
    # Verifica se algum novo inidividuo possui fitness alvo (fitness = 0)
    filhos_0 = []
    for i, fitness in enumerate(fitnesses_filhos):
        #print(f"i: {i} - fitness: {fitness}")
        if fitness == 0:
            filhos_0.append(filhos[i])
    if len(filhos_0) > 0:
        try:
            substituicao_pior(filhos, fitnesses_filhos)
        except TypeError as e:
            print(f"Error(filhos_0) !!")
            raise TypeError(e)
            #return len(filhos_0), filhos_0
        return len(filhos_0), filhos_0
    #
    
    try:
        substituicao_pior(filhos, fitnesses_filhos)
    except TypeError as e:
        print(f"Error(filhos) !!")
        raise TypeError(e)
        #return -1, ["Seleção de sobrevivente efetuada sem solução encontrada"]
    
    return 0, ["Seleção de sobrevivente efetuada sem solução encontrada"]

def algoritmo_evolutivo():
    global populacao, fitnesses, geracoes, count_fitness
    count_fitness = 0
    gerar_populacao()
    fitness_grupo(populacao)
    registro_fitnesses = []
    melhor_solucao, melhor_fitness, geracao = [], 0, 0
    
    #print("Fitnesses da população: ", fitnesses)
    
    for geracao in range(geracoes):
        print("iniciando geração #", geracao)
        # Seleção dos pais
        pai1, pai2 = selecao_pais()
        filhos = []
        # Recombinação (prob. 90%) - "cut-and-crossfill" crossover (2 filhos)
        prob = random.random()
        if prob < prob_recombinacao:
            #print(f"Recombinou!!\nProbabilidade de crossover = {prob_recombinacao}\nProbabilidade ocorrida: {prob}")
            filhos = crossover(pai1, pai2)
        else:
            #print(f"Repetiu os pais.\nProbabilidade de crossover = {prob_recombinacao}\nProbabilidade ocorrida: {prob}")
            filhos.append(pai1)
            filhos.append(pai2)
            
        # Mutação (prob. = 40%) - troca de genes
        filho_mutacao = 0
        while filho_mutacao < len(filhos):
            prob = random.random()
            if prob < prob_mutacao:
                #print(f"Filhos: {filhos}\nPasso: {filho_mutacao}")
                filhos[filho_mutacao] = mutacao(filhos[filho_mutacao])
            filho_mutacao += 1
            
        # Seleção de sobreviventes (substitui os filhos pelos piores da populacao)
            # Verifica se foi encontrado uma solução com fitness 0
        try:
            encontrou_solucao, solucoes_perfeitas = selecao_sobreviventes(filhos)
        except TypeError as e:
            print(f"Error(ae) !!")
            raise TypeError(e)
            #return [], -1, geracao
        
        fitness_medio = sum(fitnesses)/len(fitnesses)
        registro_fitnesses.append(fitness_medio)
        
        if encontrou_solucao > 0: 
            print(f"Encontrou fitness 0! {encontrou_solucao} individuo(s).")
            return solucoes_perfeitas, fitnesses[0], geracao+1, "find-sol", registro_fitnesses
        
        """Condição de término:
           *encontrar a solução
           *10.000 avaliações de Fitness
        """
        if count_fitness >= 10000:
            print("Count_fitness: ", count_fitness)
            print("Mais de 10.000 avaliações de fitness.")
            melhor_solucao.append(populacao[0])
            melhor_fitness = fitnesses[0]
            return melhor_solucao, melhor_fitness, geracao+1, "fit-max", registro_fitnesses
        
    melhor_solucao.append(populacao[0])
    melhor_fitness = fitnesses[0]
    
    return (melhor_solucao, melhor_fitness), melhor_fitness, geracao+1, "ger-max", registro_fitnesses
            
# ------------------------------------------------------------------------------ #

def main():
    geracoes_convergencia = []
    stop_reasons = []
    tempos_execucao = []
    melhores_fitness = []
    n = 30
    # Início
    
    """#Teste básico
    gerar_populacao()
    mutacao(populacao[random.randint(0, len(populacao) - 1)])
    crossover(populacao[random.randint(0, len(populacao) - 1)], populacao[random.randint(0, len(populacao) - 1)])
    print(f"Tamanho populacao: {len(populacao_ordenada)} x {len(fitnesses_ordenado)} x {len(populacao)} x {len(fitnesses)}")"""
    
    """#Teste de selecao_sobreviventes()
    gerar_populacao()
    pai1, pai2 = selecao_pais()
    filhos = crossover(pai1, pai2)
    selecao_sobreviventes(filhos)"""
    
    """
    global populacao
    solucao = populacao[random.randint(0,len(populacao))]
    
    #translate = lambda x: list(map(check_position, solucao))
    solucao_dec = [check_position(position) for position in solucao]
    #print(f"Posições: {posicoes} \n Posições_dec: {[check_position(position) for position in posicoes]}")
    print(f"\nSolução: {solucao} \nSolução decimal: {solucao_dec} \n - Fitness: {fitness(solucao)}\n")
    """ 
    
    #Teste do Algoritmo Evolutivo
    for i in range(n):
        start_time = time.time()
        melhor_solucao, melhor_fitness, geracao, stop, medias_fitger = (), 0, 0, "", 0.0
        try:
            melhor_solucao, melhor_fitness, geracao, stop, medias_fitger = algoritmo_evolutivo()
            #print(f"Fitness correspondente X População ordenada: {list(zip(fitnesses_ordenado, populacao_ordenada))}")
            #print(f"Tamanho populacao: {len(populacao_ordenada)} x {len(fitnesses_ordenado)} x {len(populacao)} x {len(fitnesses)}")
            
        except TypeError as e:
            print(f"Error(main): {e}")
            for i, individuo in enumerate(populacao):
                count = populacao.count(individuo)
                print(f"Iter {i} - Ocorrências do individuo em pop_ord: {count}\n-------------------------------------------------------{individuo}")
                
        # Fim
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n\n   -----\n   ---\n [][][][][] Fim da {i+1}ª execução [][][][][]\n\n")
        if len(melhor_solucao) == 1: print(f"Melhor solução: {melhor_solucao[0]}")
        else: print(f"Melhores soluções:\n1-{melhor_solucao[0]}\n2-{melhor_solucao[1]}")
        print(f"Melhor fitness: {melhor_fitness}\nGeração: {geracao}")
        print("Contagem de avaliações de Fitness: ", count_fitness)
    
        melhores_fitness.append(melhor_fitness)
        tempos_execucao.append(execution_time)
        geracoes_convergencia.append(geracao)
        stop_reasons.append(stop)
        fitness_medio_ger.append(medias_fitger)
        print(f"Execution time: {execution_time} seg")
        
    print(f"\n\n\n\n   -----\n   ---\n [][][][][] Fim das {n} execuções [][][][][]\n\n")
    print(f"Melhores fitnesses: {melhores_fitness}\n\nCritérios de parada: {stop_reasons}\n\nGerações: {geracoes_convergencia}\n\nTempos de execução: {tempos_execucao}\n\n")
    print(f"Tempo médio de execução: {sum(tempos_execucao)/n}\n")
    print(f"\n\nFitness médio por geração: {fitness_medio_ger}\n\n")
    for i, medias in enumerate(fitness_medio_ger):
        if i+1 < 10:
            print(f"Exec  {i+1}: {round((sum(medias)/len(medias)), 2)} fitness médio'")
        else:
            print(f"Exec {i+1}: {round((sum(medias)/len(medias)), 2)} fitness médio")
    
if __name__ == '__main__':
    main()