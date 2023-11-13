
# Resolução automatica do 8puzzle
#algoritmo A* e filas de prioridades.

from queue import PriorityQueue
#Retorna o caminho mínimo e o número de passos.
def buscaInf(inicial):
    
    final = 12345678
    passos = 0
    agenda = PriorityQueue()
    estados_past = set()
    estado = State(inicial, passos)
    agenda.put(estado)

    while not agenda.empty():
        estado = agenda.get()
        if estado.num == final:
            caminho = []
            while estado is not None:
                caminho.append(estado.ordem)
                estado = estado.antecessor
            return caminho[::-1], len(caminho)
        estados_past.add(estado.num)
        lista_trans = estado.transicoes()

        for alcancaveis in lista_trans:
            proximo = State(alcancaveis, estado.g + 1, estado)
            if proximo.num not in estados_past:
                agenda.put(proximo)
    return -1, -1

def heuristica(vet):
    #verifica valores fora do lugar (zero não conta).    
    heuristica = 0
    valor_ideal = 1
    for valor_atual in range(1, len(vet)):
        if vet[valor_atual] != valor_ideal:
            heuristica = heuristica + 1
        valor_ideal = valor_ideal + 1
    return heuristica

#gerar um atributo único para cada objeto.
def valorInt(lista):    
    inteiro = ""
    for valor_lista in lista:
        inteiro = inteiro + str(valor_lista)
    return int(inteiro)

class State:    
    #Representa um estado do jogo.
    #Inicializa um objeto Estado.
    def __init__(self, ordem, passos, antecessor=None):
        self.ordem = ordem
        self.num = valorInt(self.ordem)
        self.g = passos
        self.h = heuristica(self.ordem)
        self.f = self.g + self.h
        self.antecessor = antecessor

     #todas as transições possíveis.
    def transicoes(self):        
        vazia = self.ordem.index(0)
        alcancaveis = []

        if vazia > 2:
            new_state = self.ordem.copy()
            new_state[vazia], new_state[vazia - 3] = new_state[vazia - 3], \
                                                                         new_state[vazia]
            alcancaveis.append(new_state)

        if vazia < 6:
            new_state = self.ordem.copy()
            new_state[vazia], new_state[vazia + 3] = new_state[vazia + 3], \
                                                                         new_state[vazia]
            alcancaveis.append(new_state)

        if vazia % 3 != 0:
            new_state = self.ordem.copy()
            new_state[vazia], new_state[vazia - 1] = new_state[vazia - 1], \
                                                                         new_state[vazia]
            alcancaveis.append(new_state)

        if vazia % 3 != 2:
            new_state = self.ordem.copy()
            new_state[vazia], new_state[vazia + 1] = new_state[vazia + 1], \
                                                                         new_state[vazia]
            alcancaveis.append(new_state)
        return alcancaveis

    def __lt__(self, other):       
        return self.f <= other.f

    def __repr__(self):           
        return "{:09d}".format(self.num)#inteiro com 9 dígitos. 

