import copy

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


class Celula(object):
    def __init__(self, tipo = None, peca = None):
        self.tipo = tipo ## final= f ; fixa = fx ; parede = p ; normal = n
        self.conteudo = peca ## = peca



class Node(object):

    def __init__(self, npai = None, tbl = None, oper = None):
        self.pai = npai
        self.pecas = {}
        self.oper = oper

        if tbl is None:
            self.table = [ [Celula()]*TAMANHO["X"]]*TAMANHO["Y"]
        else:
            self.table = tbl
        
        ## copiar as pecas
        for x in self.table:
            for y in x:
                p = y.conteudo
                if p != None:
                    self.pecas[p.id] = p

    ## representasao string
    def __str__(self):
        pass
               
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
        found = search_p(id_pec)        
        if found is None:
            return None

        p = found["P"]

        if found["Y"] > 0 and found["Y"] - qty >= 0:
            # verificar que no espaco que ocupa no eixo dos XX tem possibilidade de subir a qty definida
            for x in range(p.dimensao[0]):
                for y in range(qty):
                    cel_test = self.table[found["X"] + x][found["Y"] - y]
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

            return Node(self,new_table,"move_up")

        else:
            return None


    def move_down(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para baixo 
        #tend em conta as restricoes do tamanho

        #procurar a peca
        found = search_p(id_pec)        
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

            return Node(self,new_table,"move_down")

        else:
            return None


    def move_left(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para esq 
        #tend em conta as restricoes do tamanho

        #procurar a peca
        found = search_p(id_pec)        
        if found is None:
            return None

        p = found["P"]

        if found["X"] > 0 and found["X"] - qty >= 0:
            # verificar que no espaco que ocupa no eixo dos YY tem possibilidade de subir a qty definida
            for x in range(qty):
                for y in range(p.dimensao[1]):
                    cel_test = self.table[found["X"] - x][found["Y"] + y]
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

            return Node(self,new_table,"move_left")

        else:
            return None


    def move_right(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para direita 
        #tend em conta as restricoes do tamanho

        #procurar a peca
        found = search_p(id_pec)        
        if found is None:
            return None

        p = found["P"]

        if found["X"] + p.dimensao[0] < TAMANHO["X"] and found["X"] + p.dimensao[0] + qty <=  TAMANHO["X"]:
            # verificar que no espaco que ocupa no eixo dos XX tem possibilidade de descer a qty definida
            for x in range(p.dimensao[0]):
                for y in range(qty):
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

            return Node(self,new_table,"move_right")

        else:
            return None
    

    




