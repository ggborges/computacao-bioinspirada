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
populacao = []
fitnesses = []
count_fitness = 0


def gerar_populacao():
    global tamanho_populacao, populacao
    
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
        
    #print(populacao)

def check_position(position: str):
    real_position = 0
    for index, char in enumerate(position):
        real_position += int(char) * (2**(2-index))
    
    return real_position
        
def fitness(solucao: Solucao):
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
    
def fitness_populacao(population: Populacao):
    # Gera o fitness de cada indivíduo da populacao
    fitnesses_grupo = []
    for solucao in population:
        fitnesses_grupo.append(fitness(solucao))
    
    if len(population) == len(populacao):
        fitnesses = fitnesses_grupo
        
    return fitnesses_grupo

def selecao_pais():
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
    fitnesses_roleta = sorted(fitness_populacao(roleta), reverse=True)
    return fitnesses_roleta[0], fitnesses_roleta[1]

def mutacao(individuo: Solucao):
    fst_gen = random.randint(0, len(individuo) - 1)
    snd_gen = 0
    done = False
    print(":Mutação:")
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
    
def crossover(pai1: Solucao, pai2: Solucao):
    # Cria janela de tamanho 3, 4 ou 5
    filho1, filho2 = [], []
    step = random.randint(3, 5)
    start = random.randint(0, len(pai1) - 1)
    print("Start: ", start)
    print("Step: ", step)
    if start + step > len(pai1) - 1:
        print("maior")
        
    else:
        print("menor ou igual")
    
    #print("Janela: ", window)
    
    return [filho1, filho2]
    
def algoritmo_evolutivo():
    global populacao, fitnesses, geracoes
    
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
            filhos[0] = pai1
            filhos[1] = pai2
            
            # Mutação (prob. = 40%) - troca de genes
        mutacoes = 0
        while mutacoes < len(filhos):
            prob = random.random(0,1)
            if prob < prob_mutacao:
                mutacao()
            
            # Seleção de sobreviventes (substitui os filhos pelos piores da populacao)
        """
        Condição de término:
           *encontrar a solução
           *10.000 avaliações de Fitness
        """
            
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