import numpy as np

or_op = "ou"
and_op = "e"
if_op = "se"
else_op = "então"
neg_op = "não"


# Log de saída
class Log():
    def __init__(self):
        open("log.txt", 'w').close()
        self.file = open("log.txt", "a")

    def writeNewRegister(self, line):
        self.file.write(line+"\n")


    def registerFacts(self, factbase):
        for fact in factbase.facts:
            self.writeNewRegister(f"Fato {factbase.facts.index(fact)}: {fact.list} {fact.description}")


    def registerFactBases(self, initial, final):
        self.writeNewRegister("\nBase de fatos inicial")
        self.registerFacts(initial)
        self.writeNewRegister("\nBase de fatos final")
        self.registerFacts(final)
        self.writeNewRegister("\n")



# Base de fatos
class FactBase:
    def __init__(self, facts):
        self.facts = []
        self.readFacts(facts)

    def returnFacts(self):
        list = []
        for fact in self.facts:
            list.append(f"Fato {self.facts.index(fact)}: {fact.list} {fact.description}")
        return list

    def readFacts(self, facts):
        for fact in facts:
            self.addFact(Expression(fact))

    def addFact(self, fact):
        self.facts.append(fact)

    def splitFact(self):
        for fact in self.facts:
            count_spt = 0
            if not fact.has_split and and_op in fact.list:
                array = np.array(fact.list)
                indices = np.where(array == and_op)[0]

                for i in indices:
                    new = fact.list[count_spt:i]
                    if not self.searchFact(new):
                        self.addFact(Expression(new, "Simplificação: se P e Q, então P"))
                        count_spt = i + 1
                new = fact.list[count_spt:]
                if not self.searchFact(new):
                    # print(new)
                    self.addFact(Expression(new, "Simplificação: se P e Q, então P"))
                fact.has_split = True
                return True
        return False

    def printFacts(self):
        for fact in self.facts:
            print("---------------------")
            print("Fato", self.facts.index(fact))
            fact.printExpression()

    def searchFact(self, searched):
        for fact in self.facts:
            #print(fact.var, searched)
            if fact.list == searched:
                return True
        else:
            return False


# Base de conhecimento
class KnoledgeBase:
    def __init__(self, knoledge):
        self.rules = []
        self.readRules(knoledge)

    def readRules(self, knoledge):
        c = 1
        for rule in knoledge:
            self.addRule(Rule(rule, c))
            c += 1

    def addRule(self, rule):
        self.rules.append(rule)

    def lookForward(self, q):
        for rule in self.rules:
            if rule.cons.list == q:
                #print(rule.cons.var, q.var)
                return rule
        return None

    def lookForwardExpressions(self, q):
        aux = []
        for rule in self.rules:

            if rule.cons.var == q:
                aux.append(rule)
        return aux

    def checkRulesAlreadySatisfied(self, factbase):
        for rule in self.rules:
            rule.hasbeenconfirmed = factbase.searchFact(rule.cons.list)

    def printRules(self):
        for rule in self.rules:
            print("---------------------")
            print("Regra", self.rules.index(rule))
            print("Antecedente:")
            rule.ant.printExpression()
            print("Consequente:")
            print(rule.hasbeenconfirmed)
            rule.cons.printExpression()


# Classe de regras onde temos operações se então
class Rule:
    def __init__(self, rule, index, ant = None, cons = None):
        self.rule = rule
        self.ant = ant
        self.cons = cons
        self.index = index
        self.hasbeenconfirmed = False
        self.breakTheRule()

    def breakTheRule(self):
        aux = self.rule[:]
        aux.remove('se')

        index = aux.index('então')
        self.ant = Expression(aux[0:index])
        self.cons = Expression(aux[index+1:])


# Classe de expressões
class Expression:
    def __init__(self, listq, description = ''):
        self.list = listq
        self.size = 0
        self.operations = []
        self.has_split = False
        self.description = description



    def searchExpression(self, list):
        string = ' '.join(list)
        for operation in self.operations:
            if string == operation.string:
                return operation

        return list

    def printExpression(self):
        print(self.list)


# Agente baseado em conhecimento
class KnoledgeBasedAgent:
    def __init__(self, factlist, knoledgelist, question):
        self.question = question
        self.inicialFactBase = FactBase(factlist)
        self.finalFactBase = FactBase(factlist)
        self.knoledgebase = KnoledgeBase(knoledgelist)
        self.knoledgebase.checkRulesAlreadySatisfied(self.inicialFactBase)
        self.log = Log()


    def getIndexOperatorOr(self, list):
        check = False
        count_or = 0
        array = np.array(list)
        indices = np.where(array == or_op)[0]
        # self.log.writeNewRegister(f"\nBuscando parcelas da expressão {list} do operador OU na base de fatos")
        for i in indices:
            new = list[count_or:i]
            if self.finalFactBase.searchFact(new):
                # self.log.writeNewRegister(f"Encontrado {new} na base de fatos, portanto {list} é verdadeira pela"
                #                          f"regra da ADIÇÃO onde se P, então temos P OU Q e podemos gerá-la")
                self.finalFactBase.addFact(Expression(list, 'Adição: se P, então P ou Q'))
                return True
            elif and_op in new:
                print(new)
                check = self.getIndexOperatorAnd(new)
                if check:
                    # self.log.writeNewRegister(f"Encontrado {new} na base de fatos, portanto {list} é verdadeira pela"
                    #                          f"regra da ADIÇÃO onde se P, então temos P OU Q e podemos gerá-la")
                    self.finalFactBase.addFact(Expression(list, 'Adição: se P, então P ou Q'))
                    return True

            count_or = i + 1
        new = list[count_or:]
        check  = self.finalFactBase.searchFact(new)
        if not check and and_op in new:
            check = self.getIndexOperatorAnd(new)
        if check:
            # self.log.writeNewRegister(f"\nEncontrado {new} na base de fatos, portanto {list} é verdadeira pela"
            #                          f"regra da ADIÇÃO onde se P, então temos P OU Q e podemos gerá-la")
            self.finalFactBase.addFact(Expression(list, 'Adição: se P, então P ou Q'))
        else:
            pass
            # self.log.writeNewRegister(f"\nNão foi possível encontrar nenhum dos operandos da disjunção, portanto não é"
            #                         f"possível comprovar {list}")
        return check

    def getIndexOperatorAnd(self, list):
        count_and = 0
        check = True
        array = np.array(list)
        aux = []
        indices = np.where(array == and_op)[0]
        # self.log.writeNewRegister(f"\nBuscando parcelas da expressão {list} do operador E na base de fatos")
        for i in indices:
            new = list[count_and:i]
            check = check and self.finalFactBase.searchFact(new)
            if not check and or_op in new:
                check = self.getIndexOperatorOr(new)

            if check:
                pass
                # self.log.writeNewRegister(f"Parcela da conjunção {new} encontrada na base de fatos")
            # print(check, new)
            count_and = i + 1
        new = list[count_and:]
        check = check and self.finalFactBase.searchFact(new)

        if not check and or_op in new:
            check = self.getIndexOperatorOr(new)
        if check:
            # self.log.writeNewRegister(f"Parcela da conjunção {new} encontrada na base de fatos")
            # self.log.writeNewRegister(f"\nEncontrado todas as parcelas da conjunção {list} na base de fatos, portanto"
            #                          f"podemos gerá-la pela regra da CONJUNÇÃO onde se P, Q então temos P E Q")
            self.finalFactBase.addFact(Expression(list, 'Conjunção: se P, Q, então P e Q'))

        else:
            pass
            # self.log.writeNewRegister(f"\nNão encontramos todas as parcelas da conjunção {list} na base de fatos, portanto"
            #                          f"não podemos gerá-la")
        # print(check, list[count_and:])
        return check

    def forwardChaining(self):
        # self.log.writeNewRegister("Iniciando encadeamento para frente")
        c = 1
        confirmed = False
        while not self.finalFactBase.searchFact(self.question):
            # self.log.writeNewRegister("\nEstado " + str(c))
            c += 1
            # self.log.writeNewRegister(f"Pergunta {self.question} não encontrada na base de fatos")
            satisfied_rules = []
            type_op = 0

            # Nesse ciclo é onde selecionamos as regras que podem ser satisfeitas com a base de fatos atual
            for rule in self.knoledgebase.rules:
                already_confirmed = False
                if not rule.hasbeenconfirmed:
                    # Buscando o antecedente inteiro na base de fatos
                    if self.finalFactBase.searchFact(rule.ant.list) and not already_confirmed:
                        type_op = 1
                        #rule.hasbeenconfirmed = True
                        already_confirmed = True

                    # Partindo o antecedente no operador "ou" e buscando cada uma das partes na base de fatos
                    if(or_op in rule.ant.list and not already_confirmed):
                        already_confirmed = self.getIndexOperatorOr(rule.ant.list)
                        if already_confirmed:
                            #rule.hasbeenconfirmed = True
                            type_op = 2

                    self.log.writeNewRegister(f"\n\n\n")
                    # Partindo o antecedente no operador "e" e buscando cada uma das partes na base de fatos
                    if(and_op in rule.ant.list and not already_confirmed):
                        already_confirmed = self.getIndexOperatorAnd(rule.ant.list)
                        if already_confirmed:
                            #rule.hasbeenconfirmed = True
                            type_op = 3
                    self.log.writeNewRegister(f"\n\n\n")
                    if already_confirmed:
                        satisfied_rules.append([rule, type_op])


            # self.log.writeNewRegister(f"{len(satisfied_rules)} regras satisfeitas com a base de fatos atual:")

            # Se tivermos pelo menos uma regra satisfeita cotinuamos a execução
            if len(satisfied_rules) > 0:
                controller_satisfied = False
                # nesse ciclo de repetição captaremos a primeira regra satisfeita com
                for rule_s in satisfied_rules:
                    if not rule_s[0].hasbeenconfirmed:
                        rule_s[0].hasbeenconfirmed = True
                        # self.log.writeNewRegister(f"Regra satisfeita escolhida = R{rule_s[0].index}: "
                        #                          f"{rule_s[0].rule}")
                        self.finalFactBase.addFact(Expression(rule_s[0].cons.list))
                        # self.log.writeNewRegister(f"Gerando {rule_s[0].cons.list}")
                        # self.log.writeNewRegister("Novo fato adicionado na base de fatos.")
                        controller_satisfied = True
                        break

                    else:
                        pass
                        #self.log.writeNewRegister(f"{rule_s[0].cons.list} já está na base de fatos.")

                # Talvez esse if seja desnecessário
                if(not controller_satisfied):
                    # self.log.writeNewRegister("Todas as regras satisfeitas nesse estado são redundantes.")
                    # self.log.writeNewRegister(f"Portanto {self.question} não é satisfeita através do método de "
                    #                                                        "encadeamento para frente\n")

                    print("Não foi possível chegar à pergunta através desse método.")
                    break

            # Caso contrário encerramos
            elif not self.finalFactBase.splitFact():


                # self.log.writeNewRegister("Nenhuma regra pode ser satisfeita através da base de fatos atual.")
                # self.log.writeNewRegister(f"Portanto {self.question} não é satisfeita através do método de "
                #                           "encadeamento para frente\n")

                print("Não foi possível chegar à pergunta através desse método.")
                break

        if self.finalFactBase.searchFact(self.question):
            confirmed = True
            # print(f"Através do encadeamento para frente, fica demonstrado que {self.question} é verdade.")
            # self.log.writeNewRegister(f"Portanto {self.question} é satisfeita através do método de encadeamento "
            #                                                   "para frente.\n")
        # self.log.registerFactBases(self.inicialFactBase, self.finalFactBase)
        steps = self.finalFactBase.returnFacts()
        return [confirmed, steps]

