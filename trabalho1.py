TAMANHO = {x:4,y:5}

class peca(object):
    self.id = 0 # id 
    self.dimensao = [1,2]
    self.tipo ## final ; temp ; normal


class celula(object):
    self.tipo ## final= f ; fixa = fx ; parede = parede ; normal = n
    self.conteudo ## = peca



class node(object):

    def __init__(self, npai = None, old_table = None, oper = None):
        self.pai = npai
        self.pecas = {}
        self.oper = oper

        if old_table is None:
            self.table = [ [celula()]*TAMANHO.x]*TAMANHO.y
        else:
            self.table = copy.deepcopy(old_table)
        
        ## copiar as pecas
        for x in table:
            for y in x:
                self.pecas[y.id] = y.conteudo

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
        ## se pessa final está totalmente no local final
        pass

    #verificar se estado repetido
    def repeated(self):
        ## verificar se tabela identica
        pass

    ##############
    ## MOVIMENTOS
    ##############
    def move_up(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para cima 
        #tend em conta as restricoes do tamanho
        pass

    def move_down(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para cima 
        #tend em conta as restricoes do tamanho
        pass


    def move_left(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para cima 
        #tend em conta as restricoes do tamanho
        pass


    def move_right(self, id_pec, qty):
        #verificar se na tabela a peca com o id_pec pode mover para cima 
        #tend em conta as restricoes do tamanho
        pass
    

    







tab = [ [celula()*x]*y