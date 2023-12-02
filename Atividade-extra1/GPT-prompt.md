Eu estou implementando o problema da sacola (knapsack problem) com W sendo a capacidade da mochila (W=100) e N sendo o número de itens (N=100). Eu tenho que gerar aleatoriamente os itens e a populacao. Os pesos dos itens podem variar de 1 até 50 e os lucros de 1 até 1000. Adotei a seguinte representação para os individuos: lista com 0s e 1s, representando se o item está ou não na mochila. Os indexs da lista de itens correnponte a lista de 0s e 1s que são o gene do individuo.

Como fazer uma função de fitness que penalize valores muito altos de peso total de uma solução?


Claro, vou criar um exemplo de caso de uso com subfluxo e fluxo secundário para ilustrar como esses elementos podem ser incorporados. Vamos considerar um sistema de gestão de biblioteca. O caso de uso que podemos analisar é o de "Empréstimo de Livro". Aqui está um exemplo:

**Caso de Uso: Empréstimo de Livro**

1. **Descrição:**
   - Este caso de uso descreve como um usuário pode realizar o empréstimo de um livro da biblioteca.

2. **Atores:**
   - - Usuário (Cliente)
   - - Bibliotecário

3. **Prioridade:**
   - Alta

4. **Pré-condições:**
   - - O usuário está autenticado no sistema.
   - - O livro está disponível na biblioteca.

5. **Pós-condições:**
   - - O livro é marcado como emprestado.
   - - O sistema registra o empréstimo na conta do usuário.

6. **Fluxo Principal:**
   - 1. O usuário solicita o empréstimo de um livro.
   - 2. O bibliotecário verifica a disponibilidade do livro.
   - 3. Se o livro estiver disponível, o bibliotecário registra o empréstimo.
   - 4. O sistema atualiza o status do livro para "emprestado".
   - 5. O usuário recebe o livro emprestado.

7. **Subfluxos:**
   - - **Subfluxo - Notificação de Reserva:**
     - 1. Se o livro estiver emprestado, o sistema verifica se há reservas.
     - 2. Se houver reservas, o usuário é notificado da disponibilidade do livro quando este for devolvido.

8. **Fluxo Secundário:**
   - - **Fluxo Secundário - Penalidade por Atraso:**
     - 1. Se o usuário atrasar a devolução do livro além do prazo, o sistema aplica uma penalidade.
     - 2. O bibliotecário é notificado sobre a penalidade.
     - 3. O usuário deve pagar a penalidade antes de realizar novos empréstimos.

Neste exemplo, o subfluxo "Notificação de Reserva" ocorre como parte do fluxo principal quando o livro está emprestado, mas também pode ser acionado independentemente em certas situações. O fluxo secundário "Penalidade por Atraso" descreve uma situação alternativa que pode ocorrer durante o empréstimo de livros.   