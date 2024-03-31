from copy import deepcopy
from peca import Peca

class Tabuleiro():
    def __init__(self):
        self.pecas = []
        self.qtd_colunas = 4
        self.qtd_linhas = 4
        self.tabuleiro = [[None for _ in range(self.qtd_colunas)] for _ in range(self.qtd_linhas)]
        self.pecas = [Peca(atributos) for atributos in range(16)]

    def copiar(self):
        novo_tabuleiro = Tabuleiro()
        novo_tabuleiro.tabuleiro = deepcopy(self.tabuleiro)
        novo_tabuleiro.pecas = deepcopy(self.pecas)
        return novo_tabuleiro

    def get_tabuleiro(self):
        return self.tabuleiro

    def get_pecas(self):
        return self.pecas

    def get_nomes_pecas(self):
        return ["(" + str(i) + "): " + self.pecas[i].get_nome_peca() for i in range(len(self.pecas))]

    def get_linhas(self):
        return self.tabuleiro

    def get_colunas(self):
        return [[linha[i] for linha in self.tabuleiro] for i in range(self.qtd_linhas)]

    def atributos_comuns(self, lista):
        lista_atributos = [peca.get_atributos() for peca in lista if peca]
        if len(lista_atributos) != self.qtd_linhas:
            return 0
        vitoria = 0b1111
        vitoria2 = 0b1111
        for attr in lista_atributos:
            vitoria = vitoria & attr
            vitoria2 = vitoria2 & ~attr
        return vitoria or vitoria2

    def verificar_vitoria_horizontal(self):
        for linha in self.get_linhas():
            if self.atributos_comuns(linha):
                return True
        return False

    def verificar_vitoria_vertical(self):
        lista_atrib = [[] for _ in range(self.qtd_linhas)]
        for linha in self.get_linhas():
            for i in range(len(linha)):
                lista_atrib[i].append(linha[i])
        for lista in lista_atrib:
            if self.atributos_comuns(lista):
                return True
        return False

    def verificar_vitoria_diagonal(self):
        diag_esq_dir = []
        diag_dir_esq = []
        i, j = 0, 3
        for linha in self.tabuleiro:
            diag_esq_dir += [linha[i]]
            diag_dir_esq += [linha[j]]
            i += 1
            j -= 1
        if self.atributos_comuns(diag_esq_dir) or self.atributos_comuns(diag_dir_esq):
            return True
        return False
    
    def verificar_vitoria(self):
        return any([
        self.verificar_vitoria_horizontal(),
        self.verificar_vitoria_vertical(),
        self.verificar_vitoria_diagonal(),
    ])

    def jogador(self):
        return 1 if len([peca for linha in self.tabuleiro for peca in linha if peca is not None]) % 2 == 0 else 2

    def outro_jogador(self):
        return 2 if self.jogador() == 1 else 1

    def imprimir_tabuleiro(self):
        for linha in self.tabuleiro:
            print([peca.get_abrev_peca() if peca else "____" for peca in linha])

    def colocar_peca(self, indice_peca, linha, coluna):
        peca = self.pecas[indice_peca]
        if self.tabuleiro[linha][coluna] is None and peca in self.pecas:
            self.tabuleiro[linha][coluna] = peca
            self.pecas.remove(peca)
            return True
        return False