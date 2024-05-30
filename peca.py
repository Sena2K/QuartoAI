class Peca():
    def __init__(self, atributos):
        self.atributos = atributos
        self.nome_completo = ""
        self.abreviacao = ""
        if atributos & 0b0001:
            self.nome_completo += "Alto"
            self.abreviacao += "A"
        else:
            self.nome_completo += "Baixo"
            self.abreviacao += "B"
        if atributos & 0b0010:
            self.nome_completo += " preto"
            self.abreviacao += "P"
        else:
            self.nome_completo += " branco"
            self.abreviacao += "B"
        if atributos & 0b0100:
            self.nome_completo += " círculo"
            self.abreviacao += "C"
        else:
            self.nome_completo += " quadrado"
            self.abreviacao += "Q"
        if atributos & 0b1000:
            self.nome_completo += " sólido"
            self.abreviacao += "S"
        else:
            self.nome_completo += " oco"
            self.abreviacao += "O"

    def __hash__(self):
        return hash((self.atributos, self.abreviacao))

    def __eq__(self, other):
        return isinstance(other, Peca) and self.atributos == other.atributos

    def get_atributos(self):
        return self.atributos

    def get_nome_peca(self):
        return self.nome_completo

    def get_abrev_peca(self):
        return self.abreviacao

    def estado(self):
        return self.abreviacao
