# -*- coding: UTF-8

import copy
import csv
from bot import * 
import time


TAMANHO = {"X":4,"Y":5}

class Peca(object):

    def __init__(self, id = None, dims = None, tipo = None):
        self.id = id # id 
        self.dimensao = dims #[1,2]
        self.tipo = tipo## final = f ; temp = t ; normal = n

    def __eq__(self, other): 
        if not isinstance(other, Peca):
            return False

        return self.id == other.id
    
    def __str__(self):
        return "p=[" + str(self.id) + "];"+ self.tipo


class Celula(object):
    def __init__(self, tipo = None, peca = None):
        self.tipo = tipo ## final= f ; parede = p ; normal = n
        self.conteudo = peca ## = peca
    def __str__(self):
        return "c=" + self.tipo + ";" + (str(self.conteudo) if self.conteudo != None else "p=[_];0")



class No(object):

    def __init__(self, npai = None, tbl = None, oper = None):
        self.pai = npai
        self.pecas = {}
        self.oper = oper
        self.table = []

        if tbl is None:
            col = []
            for y in range(TAMANHO["Y"]):
                col+=[Celula()]
            for x in range(TAMANHO["X"]):
                self.table += [copy.deepcopy(col)]
        else:
            self.table = tbl
        
        ## copiar as pecas
        for x in self.table:
            for y in x:
                p = y.conteudo
                if p != None:
                    self.pecas[p.id] = p

    ## representacao string
    def __str__(self):
        s = ""
        for y in range(TAMANHO["Y"]):
            for x in range(TAMANHO["X"]):
                s += str(self.table[x][y]) + " | "
            s += "\n"

        return s

    ## path de node init ate ao actual
    def path(self):
        if self.pai is None:
                return [str(self)]
        else:
                return [str(self)] + self.pai.path()
    
    # estado objectivo?
    def terminal(self):
        ## se houver alguma celula final sem uma peca final.... não é final
        
        for x in self.table:
            for cel in x:
                p = cel.conteudo
                if cel.tipo == "f":
                    if p is None:
                        return False
                    else:
                        if p.tipo != "f":
                            return False

        return True

    #verificar se estado repetido
    def repeated(self,node):
        ## verificar se tabela identica.
        ## se for retorna true no final
        ## se for encontrado alguma peca em sitio diferente 
        ##    deve se comparar com o node pai até que este seja o nó de origem
        for x in range(TAMANHO["X"]):
            for y in range(TAMANHO["Y"]):
                cel = self.table[x][y]
                cel_orig = node.table[x][y]
                if cel.conteudo != cel_orig.conteudo:
                    if self.pai is None:
                        return False
                    else:
                        return self.pai.repeated(node)
        return True
    #procurar na table as coords e a propria peca pelo ID
    def search_p(self, id_pec):
        for x in range(TAMANHO["X"]):
            for y in range(TAMANHO["Y"]):
                cel = self.table[x][y]
                if cel.conteudo != None and cel.conteudo.id == id_pec:
                    return {"X":x,"Y":y,"P":cel.conteudo}

        return None

    ##############
    ## MOVIMENTOS
    ##############
    def move_up(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para cima 
        #tend em conta as restricoes do tamanho

        #procurar a peca
        found = self.search_p(id_pec)        
        if found is None:
            return None

        p = found["P"]

        if found["Y"] > 0 and found["Y"] - qty >= 0:
            # verificar que no espaco que ocupa no eixo dos XX tem possibilidade de subir a qty definida
            for x in range(p.dimensao[0]):
                for y in range(qty):
                    cel_test = self.table[found["X"] + x][found["Y"] - y - 1]
                    # desde que a celula não seja uma parede e estiver vazia, a peca pode se mover para la
                    if cel_test.conteudo != None or cel_test.tipo == "P":
                        return None
            
            # clone table
            new_table = copy.deepcopy(self.table)
            #temos de copiar outra vez por causa do deepcopy
            p = new_table[found["X"]][found["Y"]].conteudo
            
            #remover das celulas de onde se moveu
            for x in range(p.dimensao[0]):
                for y in range(p.dimensao[1]):
                    new_table[x+found["X"]][y+found["Y"]].conteudo = None

            # add peca do all cells 
            for x in range(p.dimensao[0]):
                for y in range(p.dimensao[1]):
                    new_table[x+found["X"]][y+found["Y"] - qty].conteudo = p

            return No(self,new_table,"move_up")

        else:
            return None


    def move_down(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para baixo 
        #tend em conta as restricoes do tamanho

        #procurar a peca
        found = self.search_p(id_pec)        
        if found is None:
            return None

        p = found["P"]

        if found["Y"] + p.dimensao[1] < TAMANHO["Y"] and found["Y"] + p.dimensao[1] + qty <=  TAMANHO["Y"]:
            # verificar que no espaco que ocupa no eixo dos XX tem possibilidade de descer a qty definida
            for x in range(p.dimensao[0]):
                for y in range(qty):
                    cel_test = self.table[found["X"] + x][found["Y"] + p.dimensao[1] + y]
                    # desde que a celula não seja uma parede e estiver vazia, a peca pode se mover para la
                    if cel_test.conteudo != None or cel_test.tipo == "P":
                        return None
            
            # clone table
            new_table = copy.deepcopy(self.table)
            #temos de copiar outra vez por causa do deepcopy
            p = new_table[found["X"]][found["Y"]].conteudo
            
            #remover das celulas de onde se moveu
            for x in range(p.dimensao[0]):
                for y in range(p.dimensao[1]):
                    new_table[x+found["X"]][y+found["Y"]].conteudo = None

            # add peca do all cells 
            for x in range(p.dimensao[0]):
                for y in range(p.dimensao[1]):
                    new_table[x+found["X"]][y+found["Y"] + qty].conteudo = p

            return No(self,new_table,"move_down")

        else:
            return None


    def move_left(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para esq 
        #tend em conta as restricoes do tamanho

        #procurar a peca
        found = self.search_p(id_pec)        
        if found is None:
            return None

        p = found["P"]

        if found["X"] > 0 and found["X"] - qty >= 0:
            # verificar que no espaco que ocupa no eixo dos YY tem possibilidade de subir a qty definida
            for x in range(qty):

                for y in range(p.dimensao[1]):
                    print(3)
                    cel_test = self.table[found["X"] - x-1][found["Y"] + y]
                    print(str(cel_test))
                    # desde que a celula não seja uma parede e estiver vazia, a peca pode se mover para la
                    if cel_test.conteudo != None or cel_test.tipo == "P":
                        return None
            
            # clone table
            new_table = copy.deepcopy(self.table)
            #temos de copiar outra vez por causa do deepcopy
            p = new_table[found["X"]][found["Y"]].conteudo
            
            #remover das celulas de onde se moveu
            for x in range(p.dimensao[0]):
                for y in range(p.dimensao[1]):
                    new_table[x+found["X"]][y+found["Y"]].conteudo = None

            # add peca do all cells 
            for x in range(p.dimensao[0]):
                for y in range(p.dimensao[1]):
                    new_table[x+found["X"] - qty][y+found["Y"]].conteudo = p

            return No(self,new_table,"move_left")

        else:
            return None


    def move_right(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para direita 
        #tendo em conta as restricoes do tamanho

        #procurar a peca
        found = self.search_p(id_pec)        
        if found is None:
            return None

        p = found["P"]

        if found["X"] + p.dimensao[0] < TAMANHO["X"] and found["X"] + p.dimensao[0] + qty <=  TAMANHO["X"]:
            # verificar que no espaco que ocupa no eixo dos XX tem possibilidade de descer a qty definida
            for x in range(qty):
                for y in range(p.dimensao[1]):
                    cel_test = self.table[found["X"] + p.dimensao[0] + x][found["Y"] + y]
                    # desde que a celula não seja uma parede e estiver vazia, a peca pode se mover para la
                    if cel_test.conteudo != None or cel_test.tipo == "P":
                        return None
            
            # clone table
            new_table = copy.deepcopy(self.table)
            #temos de copiar outra vez por causa do deepcopy
            p = new_table[found["X"]][found["Y"]].conteudo
            
            #remover das celulas de onde se moveu
            for x in range(p.dimensao[0]):
                for y in range(p.dimensao[1]):
                    new_table[x+found["X"]][y+found["Y"]].conteudo = None

            # add peca do all cells 
            for x in range(p.dimensao[0]):
                for y in range(p.dimensao[1]):
                    new_table[x+found["X"] + qty][y+found["Y"]].conteudo = p

            return No(self,new_table,"move_right")

        else:
            return None
    
#d;4;5
#p;2;3;1;n
#t;n,2;n,2;n,2;n,0
def node_from_csv(file = 'default.csv'):
    base_node = None
    y = 0
    pieces = {}
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        for row in reader:
            #dims
            if(row[0] == 'd' and len(row) == 3):
                TAMANHO["X"] = int(row[1],base=10)
                TAMANHO["Y"] = int(row[2],base=10)
                base_node = No()
                pieces = base_node.pecas
            #pecas
            elif(row[0] == 'p' and len(row) == 5):
                id = int(row[1],base=10)
                dim = [int(row[2],base=10),int(row[3],base=10)]                
                pieces[id] = Peca(id=id,dims=dim,tipo=row[4])
            #linhas da matriz
            elif(row[0] == 't' and len(row) == TAMANHO["X"]+1):
                for i in range(TAMANHO["X"]):
                    c = row[i+1].split(",")
                    base_node.table[i][y].tipo = c[0]
                    id = int(c[1],base=10)
                    if id != 0:
                        base_node.table[i][y].conteudo = pieces[id]
                y+=1

    
    return base_node


#print a board representation of a state from a list
def print_board(node, state):
    for idx in range(len(state)):
        if idx%4 == 0:
            print()
        piece = state[idx]
        c_type = node.table[idx%4][idx//4].tipo
        c_content = "p=[" + str(piece) + "];" + ("f" if piece == 1 else "n")
        print("c=" + c_type + ";" + (str(c_content) if piece != 0 else "p=[_];0") + ' | ', end='')

#string representation of a piece movement
def move_as_string(move):
    #check if piece id has 1 or 2 digits
    if move[1].isdigit():
        delim = 2
    else:
        delim = 1
    id_piece = move[:delim]
    direction = move[delim:]

    return "Move " + direction + " the piece with ID=" + id_piece

def init():
    bnode = node_from_csv('easy.csv')
    while True:
        print(str(bnode))
        print("move")
        id = int(input("id? "),10)
        direction = input("direction?(wasd) ")
        
        if direction == "a":
            n = bnode.move_left(id,1)
            if n == None:
                print("invalid move")
            else:
                bnode = n
        elif direction == "d":
            n = bnode.move_right(id,1)
            if n == None:
                print("invalid move")
            else:
                bnode = n
        elif direction == "w":
            n = bnode.move_up(id,1)
            if n == None:
                print("invalid move")
            else:
                bnode = n
        elif direction == "s":
            n = bnode.move_down(id,1)
            if n == None:
                print("invalid move")
            else:
                bnode = n
        
        if  bnode.terminal():
            print(str(bnode))
            print("CONGRATULATIONS YOU WON!!")
            break
    

## Começa Aqui o Programa em Execução
print("")
print("###########################################")
print("############# KLOTSKI FOR IART ############")
print("###########################################")
print("")
print("")
print("Bem-vindo ao Programa de resolução do puzzle Klotski!")
print("")
print("Por favor selecione uma das seguintes opções:")
print("1 - Resolver manualmente o puzzle.")
print("2 - Resolver através de uma pesquisa em largura.")
print("3 - Resolver através de uma pesquisa em profundidade.")
print("4 - Resolver através de uma pesquisa com aprofundamento progressivo.")
print("5 - Resolver através de uma pesquisa gulosa.")
print("6 - Resolver através de uma pesquisa com Algoritmo A* (heuristica Manhattan).")
print("7 - Resolver através de uma pesquisa com Algoritmo A* (heuristica Soma).")
print("")
mode = int(input('Escolha uma opção: '))

if mode == 1:
    init()
else:
    node = node_from_csv('medium.csv')
    board = node.table
    pieces = node.pecas
    goal_index = None
    state = [None] * 20                           #put in list format for the Klotski solver
    for column in board:
        for cell in column:
            if cell.tipo == 'f' and goal_index == None:
                goal_index = 4 * column.index(cell) + board.index(column)
            if cell.conteudo == None:
                state[4 * column.index(cell) + board.index(column)] = 0
            else:
                state[4 * column.index(cell) + board.index(column)] = cell.conteudo.id
    puzzle = Klotski(tuple(state),goal_index)

    print(str(node))
    print("Resolvendo...")

    start_time = time.time()

    if mode == 2:
        search = breadth_first_graph_search(puzzle)
        moves = search.solution()
        states = search.solution_states()
        for idx in range(len(states)):
            print("\n\n\n" + move_as_string(moves[idx]))
            print_board(node, states[idx])
        print("\n\nbfs: " + str(moves))
    elif mode == 3:
        search = depth_first_graph_search(puzzle)
        moves = search.solution()
        states = search.solution_states()
        for idx in range(len(states)):
            print("\n\n\n" + move_as_string(moves[idx]))
            print_board(node, states[idx])
        print("\n\ndfs: " + str(moves))
    elif mode == 4:
        search = iterative_deepening_search(puzzle)
        moves = search.solution()
        states = search.solution_states()
        for idx in range(len(states)):
            print("\n\n\n" + move_as_string(moves[idx]))
            print_board(node, states[idx])
        print("\n\niterative: " + str(moves))
    elif mode == 5:
        search = greedy_best_first_graph_search(puzzle,lambda n: n.path_cost + heuristic_manhattan(n,goal_index))
        moves = search.solution()
        states = search.solution_states()
        for idx in range(len(states)):
            print("\n\n\n" + move_as_string(moves[idx]))
            print_board(node, states[idx])
        print("\n\ngreedy: " + str(moves))
    elif mode == 6:
        search = astar_search(puzzle)
        moves = search.solution()
        states = search.solution_states()
        for idx in range(len(states)):
            print("\n\n\n" + move_as_string(moves[idx]))
            print_board(node, states[idx])
        print("\n\nA* (h1): " + str(moves))
    elif mode == 7:
        search = astar_search(puzzle,lambda n: n.path_cost + heuristic_pieces_sum(n,goal_index))
        moves = search.solution()
        states = search.solution_states()
        for idx in range(len(states)):
            print("\n\n\n" + move_as_string(moves[idx]))
            print_board(node, states[idx])
        print("\n\nA* (h2): " + str(moves))
    else:
        print("Invalid option")
        exit

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Explored nodes: " + str(Node.explored_nodes))