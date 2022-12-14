class Solver:
    def __init__(self):
        self.or_op = "ou"
        self.and_op = "e"
        self.if_op = "se"
        self.else_op = "então"
        self.neg_op = "não"

    @staticmethod
    def filterList(lista):
        for i in range(len(lista)):

            lista[i] = lista[i].lower()

        if "end" in lista:
            lista.remove('end')

    # Método que divide a expressão em um operador específico
    def splitExpression(self, lista, op):
        new = lista[:]
        if self.if_op in lista:
            new.remove(self.if_op)
        split_index = new.index(op)

        return [new[0:split_index], new[split_index+1: len(new)]]

    # Método que aplica a equivalência p -> q : ~p V q
    def convertExpression(self, lista):
        new = lista[:]
        if self.if_op in new:
            steps = []
            expression = self.splitExpression(new, self.else_op)
            ant = expression[0]
            con = expression[1]
            steps.append(f"O antecedente (p) da expressão é{ant} e o consequente(q) da expressão é{con}")
            new_ant = self.neg(ant)
            steps.append(f"Portanto negamos o antecedente (p) {ant} e obtemos(~p) {new_ant}")
            con.insert(0, self.or_op)
            steps.append(f"Observe que nessa relação o consequente não sofre alterações.")
            steps.append(f"Portanto basta apenas associarmos o novo antecedente ao mesmo consequente como dois "
                         f"elementos de uma disjunção, obtendo assim: ~p ou q")
            new_ant.extend(con)
            # print(new_ant)
            return ["p -> q = ~p V q", steps, new_ant]

    # Método que aplica a equivalência p -> q : ~q -> ~p (contrapositiva)
    def convertExpression2(self, lista):
        # print(" ".join(lista))
        new = lista[:]
        negacao = []
        if self.if_op in lista:
            steps = []
            expression = self.splitExpression(new, self.else_op)

            ant = expression[0]
            con = expression[1]
            steps.append(f"O antecedente (p) da expressão é{ant} e o consequente(q) da expressão é{con}")
            # print(ant, con)
            steps.append(f"Para realizarmos a contrapositiva, devemos inverter essa relação ao passo que negamos as proposições")
            new_ant = self.neg(con)
            steps.append(f"Portanto, o novo antecedente será a negação do antigo consequente, portanto ~q: {new_ant}")
            new_ant.insert(0, self.if_op)
            new_con = self.neg(ant)
            steps.append(f"Enquanto que o novo consequente será a negação do antigo antecedente, portanto ~p: {new_con}")
            new_con.insert(0, self.else_op)
            steps.append(f"Concluímos então associando as proposições nessa nova ordem: se ~q então p")
            new_ant.extend(new_con)
            negacao = new_ant
            return ["p -> q = ~q -> ~p", steps, new_ant]

    # Método que aplica a equivalência ~p V q -> p -> q
    def convertExpression3(self, lista):
        steps = []
        new = lista[:]
        if self.if_op not in new:
            expression = self.splitExpression(new, self.or_op)
            ant = expression[0]
            con = expression[1]
            steps.append(f"O antecedente (p) da expressão é{ant} e o consequente(q) da expressão é{con}")
            new_ant = self.neg(ant)
            steps.append(f"Portanto negamos o antecedente (~p) {ant} e obtemos(p) {new_ant}, pois ~(~p) = p")
            steps.append(f"Observe que nessa relação o consequente não sofre alterações.")
            steps.append(f"Portanto basta apenas associarmos o novo antecedente ao mesmo consequente como dois "
                         f"elementos de uma expressão se então, obtendo assim: p -> q")
            ant.insert(0, self.if_op)
            con.insert(0, self.else_op)
            new_ant.extend(con)
            # print(new_ant)
            return ["~p V q -> p -> q", steps, new_ant]

    # Método que aplica a negação sobre todos os componentes da expressão
    def neg(self, lista):
        i = 0
        new = lista[:]
        c = len(new)
        while i < c:
            if new[i] == self.and_op:
                new[i] = self.or_op

            elif new[i] == self.or_op:
                new[i] = self.and_op

            elif new[i] == self.neg_op:
                del new[i]
                c = len(new)

            else:
                new.insert(i, self.neg_op)
                c = len(new)
                i += 1
            # print(lista, i, c)
            i += 1
        return new

    # Método que faz o controle da negação, convertendo a condicional se necessário antes de aplicar
    def negExpression(self, lista):
        # print(" ".join(lista))
        new = lista[:]
        negacao = []
        if self.if_op in lista:
            eq = self.convertExpression(new)
            new = eq[2]
            # print(new_exp)

        negacao = self.neg(new)
        # print(" ".join(negacao))
        return negacao

    # Método que retorna todas as possíveis equivalências da preposição passada
    def returnAllEquivalencies(self, lista):
        self.filterList(lista)
        eq1 = lista[:]
        eq2 = lista[:]

        dict = {}
        if self.if_op in lista:
            # print("\nPara a preposição passada existem 2 possíveis equivalências: ")
            dict['1'] = self.convertExpression(eq1)
            # print("\n1 - se p então q = ~p ou q")
            # print("\n2 - se p então q = se ~q então ~p")
            dict['2'] = self.convertExpression(eq2)
            # unecessary ~p ou q = q ou ~p
            # print("\n3 - se p então q = q ou ~p")
            # eq3 = self.convertExpression(eq2)
            # print(eq3)

        elif self.or_op in lista:
            # print("\nPara a preposição passada existem 3 possíveis equivalências: ")
            # print("\n1 - ~p ou q = se p então q")
            eq1 = self.convertExpression3(eq1)
            dict['1'] = eq1
            # print(eq1)
            # print("\n2 - se p então q = se ~q então ~p")
            eq2 = self.convertExpression2(eq1[2])
            dict['2'] = eq2
        #print(dict)
            # unecessary ~p ou q = q ou ~p
            # print("\n3 - se ~q então ~p = q ou ~p")
            # eq3 = self.convertExpression(eq2)
            # print(eq3)
        return dict

    # Método que retorna todas as possíveis negação da preposição passada
    def returnAllDenials(self, lista):
        self.filterList(lista)
        new = lista[:]
        dictn = {}

        if self.if_op in lista:
            print("\nPara a preposição passada existem 2 possíveis negações: ")
            print("\n1 - a negação após convertê-la com a relação se p então q = ~p ou q")
            dictn['1'] = self.negExpression(new)
            print("\n2 - a negação da sua contrapositiva")
            #conv = self.convertExpression2(new)
            #dictn['2'] = self.negExpression(conv[2])

        else:
            dictn['1'] = self.negExpression(new)

        return dictn
