class Peca():
    def __init__(self, atributos):
        self.atributos = atributos
        self.nome_completo = ""
        self.abreviacao = ""
        if atributos & 0b0001:
            self.nome_completo += "Alta"
            self.abreviacao += "A"
        else:
            self.nome_completo += "Baixa"
            self.abreviacao += "B"
        if atributos & 0b0010:
            self.nome_completo += " preta"
            self.abreviacao += "P"
        else:
            self.nome_completo += " branca"
            self.abreviacao += "B"
        if atributos & 0b0100:
            self.nome_completo += " círculo"
            self.abreviacao += "C"
        else:
            self.nome_completo += " quadrado"
            self.abreviacao += "Q"
        if atributos & 0b1000:
            self.nome_completo += " sólida"
            self.abreviacao += "S"
        else:
            self.nome_completo += " oca"
            self.abreviacao += "O"

    def get_atributos(self):
        return self.atributos

    def get_nome_peca(self):
        return self.nome_completo

    def get_abrev_peca(self):
        return self.abreviacao