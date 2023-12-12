class AlgoritmoGenetico:
    
    def crossfill(pai1: Solucao, pai2: Solucao, start: int, step: int, step2: int = 0):
        filho = []
        #steps1 = [0, step2]
        #steps2 = [start, step]
        print(f"Start: {start} / Step: {step} / Step2: {step2}")
        step_pai2 = 0
        for i in range(len(pai1)):
            if i not in range(start, start + step) and i not in range(0, step2):
                print("(pai2)Indicie crossfill: ", i)
                if pai2[i] in filho:
                    filho.append(pai2[i])
            else:
                print("(pai1)Indicie crossfill: ", i)
                filho.append(pai1[i])
                
            step_pai2 += 1
        
        return filho
    
    def crossover(pai1: Solucao, pai2: Solucao):
        print("\n---------------------------\n..::Crossover::..")
        # Cria janela de tamanho 3, 4 ou 5
        filhos = [Solucao, Solucao]
        step = random.randint(3, 5)
        start = random.randint(0, len(pai1) - 1)
        print("Start: ", start)
        print("Step: ", step)
        if start + step > len(pai1) - 1:
            print("maior")
            step2 = (step - (len(pai1) - start))
            step = len(pai1) - start
            for i in range(1):
                filhos[i] = crossfill(pai1, pai2, start, step, step2)
        else:
            print("menor ou igual")
            for i in range(1):
                filhos[i] = crossfill(pai1, pai2, start, step)
        
        #print("Janela: ", window)
        
        print(f"Pai 1: {pai1}\nPai 2: {pai2}")
        print(f" = Filho 1: {filhos[0]}\n = Filho 2: {filhos[1]}")
        return filhos
    
    def substituicao_pior(filhos, fitnesses_filhos):
    global populacao, fitnesses, populacao_ordenada, fitnesses_ordenado
    print(f"População: {len(populacao)} - Fitnesses: {len(fitnesses)}")
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
    #print(f"Fitnesses aux: {fitnesses_aux}\nTamanho fit aux: {len(fitnesses_aux)}")
    #print(f"Populacao aux: {populacao_aux}\nTamanho pop aux: {len(populacao_aux)}")
    
    fitnesses_ordenado = fitnesses_aux[:100]
    populacao_ordenada = populacao_aux[:100]
    #print(f"Fitnesses ordenado: {fitnesses_ordenado}\nTamanho fit ord: {len(fitnesses_ordenado)}")
    print(f"Tamanho pop ord: {len(populacao_ordenada)}")
    
    fitnesses, populacao = [], []
    print(f"Tamanho pop: {len(populacao)} - Tamanho fit: {len(fitnesses)}")
    for ind, par in enumerate(pares):
        if par[1] in populacao_ordenada:
            fitnesses.append(par[0])
            populacao.append(par[1])
            if ind > 97:
                print(f"Par: {par}")
                print(f"for: {ind}\nlen(pop): {len(populacao)}\nlen(fit): {len(fitnesses)}")
    
    #print(f"Fitnesses: {fitnesses}\nTamanho fit: {len(fitnesses)}")
    #print(f"Populacao: {populacao}\nTamanho pop: {len(populacao)}")
    
    if len(populacao) == len(populacao_ordenada) and len(populacao) == 100:
        print("Ok!") 
    else:         
        str_erro = f"Erro com tamanho da população.\nlen(pop): {len(populacao)} - len(pop_ord): {len(populacao_ordenada)}\n len(fit): {len(fitnesses)} - len(fit_ord): {len(fitnesses_ordenado)}\n"
        str_objetos = f"População: {populacao}\nPopul ord: {populacao_ordenada}"
        raise TypeError(str_erro+str_objetos)
    
    #print("População: ", len(populacao))
    #print("Fitnesses: ", len(fitnesses))
    #print("População ordenada: ", len(populacao_ordenada))
    #print("Fitnesses ordenado: ", len(fitnesses_ordenado))