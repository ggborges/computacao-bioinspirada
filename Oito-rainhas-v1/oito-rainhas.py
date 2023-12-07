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
import random, time
from itertools import permutations
from typing import List


Solucao = List[str]
Populacao = List[Solucao]

tamanho_populacao = 100
geracoes = 100
prob_recombinacao = 0.9
prob_mutacao = 0.4
posicoes = ["000", "001", "010", "011", "100", "101", "110", "111"]
populacao = Populacao
populacao_ordenada = Populacao
fitnesses = []
fitnesses_ordenado = []
count_fitness = 0


def gerar_populacao():
    print("\n---------------------------\n..::Gerar população::..")
    global tamanho_populacao, populacao, fitnesses, fitnesses_ordenado, populacao_ordenada
    
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
        populacao.append(solucao)
    
    fitnesses = fitness_grupo(populacao)
    pares = list(zip(fitnesses, populacao))
    pares_ordenados = sorted(pares, key=lambda x: x[0])
    fitnesses_ordenado = [par[0] for par in pares_ordenados]
    populacao_ordenada = [par[1] for par in pares_ordenados]

def check_position(position: str):
    real_position = 0
    for index, char in enumerate(position):
        real_position += int(char) * (2**(2-index))
    
    return real_position
        
def fitness(solucao: Solucao):
    print("\n---------------------------\n..::Fitness:..")
    global count_fitness
    count_fitness += 1
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
    
    # Escolher 5 indivíduos aleatoriamente com igual probabilidade
    while len(roleta) < 5:
        i_random = random.randint(0, len(populacao)-1)
        escolhido = populacao[i_random]
        if escolhido not in roleta:
            roleta.append()
            
    pai1, pai2 = roleta(roleta)
        
    return pai1, pai2

def roleta(roleta: List[List[str]]):
    print("\n---------------------------\n..::Roleta::..")
    fitnesses_roleta = sorted(fitness_populacao(roleta), reverse=True)
    return fitnesses_roleta[0], fitnesses_roleta[1]

def mutacao(individuo: Solucao):
    fst_gen = random.randint(0, len(individuo) - 1)
    snd_gen = 0
    done = False
    print("\n---------------------------\n..::Mutação::..")
    print(f"Solução original:\n - {individuo}\n\n")
    while not done:
        snd_gen = random.randint(0, len(individuo) - 1)
        if(snd_gen != fst_gen):
            done = True
    
    aux = individuo[snd_gen]
    individuo[snd_gen] = individuo[fst_gen]
    individuo[fst_gen] = aux
    print(". .. ... mutação em andamento ... .. .")
    print(f"Solução mutante:\n - {individuo}\n\n")

def crossfill(corte_pai, pai: Solucao):
    filho = Solucao
    filho = corte_pai
    #for i in range(len(corte_pai), (len(pai) - len(corte_pai)))
    i = len(corte_pai)
    while len(filho) < 8:
        print("Pai[i]: ", pai[i])
        print("Filho: ", filho)
        if pai[i] not in filho: filho.append(pai[i])
        if i < 7: i += 1
        else: i = 0
    
    print("Filho: ", filho)
    return filho

def crossover(pai1: Solucao, pai2: Solucao):
    filhos = [Solucao, Solucao]
    ponto_corte = random.randint(0, len(pai1))
    corte1 = pai1[:ponto_corte]
    corte2 = pai2[:ponto_corte]
    print(f"Pai1: {pai1}\nPai2: {pai2}\nPonto de corte: {ponto_corte}\n")
    print(f"Corte do pai 1: {corte1}\nCorte do pai 2: {corte2}\n")
    filho1 = crossfill(corte1, pai2)
    filho2 = crossfill(corte2, pai1)
    filhos = [filho1, filho2]
    
    return filhos

def selecao_sobreviventes(filhos: [Solucao, Solucao]):
    print("\n---------------------------\n..::Seleção de sobreviventes::..")
    global populacao, fitnesses, populacao_ordenada, fitnesses_ordenado
    fitnesses_filhos = fitness_grupo(filhos)
    # Verifica se algum novo inidividuo possui fitness alvo (fitness = 0)
    filhos_0 = []
    for i, fitness in enumerate(fitnesses_filhos):
        if fitness == 0:
            filhos_0.append(filhos[i])
    if len(filhos_0) > 0:
        return len(filhos_0), filhos_0
    #
    fitnesses_aux = fitnesses + fitnesses_filhos
    print("Fitnesses dos filhos: ", fitnesses_filhos)
    populacao_aux = populacao + filhos
    pares = list(zip(fitnesses_aux, populacao_aux))
    pares_ordenados = sorted(pares, key=lambda x: x[0])
    
    fitnesses_aux = [par[0] for par in pares_ordenados]
    populacao_aux = [par[1] for par in pares_ordenados]
    
    populacao_ordenada = populacao_aux[:len(populacao)-1]
    fitnesses_ordenado = fitnesses_aux[:len(fitnesses)-1]
        
    populacao = [par[1] for par in pares if par[1] in populacao_ordenada]
    fitnesses = [par[0] for par in pares if par[1] in populacao_ordenada]
    
    print("Ok!") if len(populacao) == len(populacao_aux) else print("Fail!")
    print("População: ", populacao)
    print("Fitnesses: ", fitnesses)
    print("População ordenada: ", populacao_ordenada)
    print("Fitnesses ordenado: ", fitnesses_ordenado)
    
    return 0, ["Seleção de sobrevivente efetuada sem solução encontrada"]

def algoritmo_evolutivo():
    global populacao, fitnesses, geracoes, count_fitness
    
    gerar_populacao()
    fitness_grupo(populacao)
    
    print("Fitnesses da população: ", fitnesses)
    
    for geracao in range(geracoes):
        # Seleção dos pais
        pai1, pai2 = selecao_pais()
        filhos = [Solucao, Solucao]
        # Recombinação (prob. 90%) - "cut-and-crossfill" crossover (2 filhos)
        prob = random.random(0,1)
        if prob < prob_recombinacao:
            print(f"Recombinou!!\nProbabilidade de crossover = {prob_recombinacao}\nProbabilidade ocorrida: {prob}")
            filhos = crossover(pai1, pai2)
        else:
            print(f"Repetiu os pais.\nProbabilidade de crossover = {prob_recombinacao}\nProbabilidade ocorrida: {prob}")
            filhos.append(pai1)
            filhos.append(pai2)
            
        # Mutação (prob. = 40%) - troca de genes
        mutacoes = 0
        while mutacoes < len(filhos):
            prob = random.random(0,1)
            if prob < prob_mutacao:
                mutacao()
            
        # Seleção de sobreviventes (substitui os filhos pelos piores da populacao)
            # Verifica se foi encontrado uma solução com fitness 0
        encontrou_solucao, solucoes_perfeitas = selecao_sobreviventes(filhos)
        if encontrou_solucao > 0: 
            print(f"Encontrou fitness 0! {encontrou_solucao} individuo(s).")
            return filhos, geracao
        
        """
        Condição de término:
           *encontrar a solução
           *10.000 avaliações de Fitness
        """
        if count_fitness >= 10.000:
            print("Mais de 10.000 avaliações de fitness.")
            melhor_solucao = populacao_ordenada[0]
            return melhor_solucao, , geracao
        
    melhor_solucao = populacao_ordenada[0]
    melhor_fitness = fitnesses_ordenado[0]
            
# ------------------------------------------------------------------------------ #

def main():
    start_time = time.time()
    # Início
    
    gerar_populacao()
    mutacao(populacao[random.randint(0, len(populacao) - 1)])
    crossover(populacao[random.randint(0, len(populacao) - 1)], populacao[random.randint(0, len(populacao) - 1)])
    
    """
    global populacao
    solucao = populacao[random.randint(0,len(populacao))]
    
    #translate = lambda x: list(map(check_position, solucao))
    solucao_dec = [check_position(position) for position in solucao]
    #print(f"Posições: {posicoes} \n Posições_dec: {[check_position(position) for position in posicoes]}")
    print(f"\nSolução: {solucao} \nSolução decimal: {solucao_dec} \n - Fitness: {fitness(solucao)}\n")
    """ 
    
    # Fim
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seg")
    
if __name__ == '__main__':
    main()