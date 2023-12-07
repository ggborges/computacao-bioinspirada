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