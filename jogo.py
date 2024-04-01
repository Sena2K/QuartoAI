from tabuleiro import Tabuleiro
from quartoEnum import Quarto

def primitivo(estado):
    if estado.verificar_vitoria_horizontal() or estado.verificar_vitoria_vertical() or estado.verificar_vitoria_diagonal():
        return Quarto.VITORIA
    if all(peca is not None for linha in estado.get_tabuleiro() for peca in linha):
        return Quarto.EMPATE
    return Quarto.INDECISO

def gerar_movimentos(estado):
    movimentos = []
    for i, peca in enumerate(estado.get_pecas()):
        if peca:  # Verifica se a peça não está no tabuleiro
            for linha in range(estado.qtd_linhas):
                for coluna in range(estado.qtd_colunas):
                    if estado.get_tabuleiro()[linha][coluna] is None:  # Lugar está vazio
                        movimentos.append((i, linha, coluna))
    return movimentos

def fazer_movimento(movimento, estado):
    indice_peca, linha, coluna = movimento
    if estado.colocar_peca(indice_peca, linha, coluna):
        return estado
    return None

def avaliar(estado):
    resultado = primitivo(estado)
    if resultado == Quarto.VITORIA:
        return 1  # Vitória
    elif resultado == Quarto.EMPATE:
        return 0  # Empate
    else:
        return -1  # Indeciso ou derrota

def avaliar_heuristica(estado):
    """
    Avalia o estado do tabuleiro usando uma abordagem heurística que
    leva em conta vitórias potenciais, bloqueios e posições neutras.
    """
    pontuacao = 0
    # Verifica linhas, colunas e as duas diagonais
    for linha in estado.get_linhas():
        pontuacao += atributos_comuns_heuristica(linha)
    for coluna in estado.get_colunas():
        pontuacao += atributos_comuns_heuristica(coluna)
    pontuacao += atributos_comuns_heuristica([estado.tabuleiro[i][i] for i in range(estado.qtd_linhas)])
    pontuacao += atributos_comuns_heuristica([estado.tabuleiro[i][estado.qtd_linhas - i - 1] for i in range(estado.qtd_linhas)])
    
    # Diferencia entre jogador maximizando e minimizando
    if estado.jogador() == 1:
        return pontuacao
    else:
        return -pontuacao
    
def atributos_comuns_heuristica(lista):
    """
    Calcula a pontuação heurística para uma lista de peças baseada na presença de atributos comuns.
    """
    if not lista or all(peca is None for peca in lista):
        return 0  # Se a lista estiver vazia ou contiver apenas None, retorna 0.
    
    pontuacao = 0
    atributos_compartilhados = 0b1111
    atributos_opostos = 0b1111
    num_pecas = 0

    for peca in lista:
        if peca is not None:
            atributos_compartilhados &= peca.get_atributos()
            atributos_opostos &= ~peca.get_atributos()
            num_pecas += 1

    # Verifica se há atributos compartilhados entre todas as peças não vazias
    if atributos_compartilhados != 0:
        pontuacao += num_pecas  # A pontuação aumenta com o número de peças com atributos compartilhados

    # Verifica se os atributos opostos formariam uma linha completa
    if atributos_opostos != 0:
        pontuacao += num_pecas  # Similarmente, aumenta a pontuação se houver potencial para atributos opostos

    return pontuacao    

def minimax(estado, profundidade, alfa, beta, maximizandoJogador):
    if profundidade == 0 or primitivo(estado) != Quarto.INDECISO:
        return avaliar_heuristica(estado), None

    if maximizandoJogador:
        maxAval = float('-inf')
        melhorMovimento = None
        for movimento in gerar_movimentos(estado):
            novoEstado = fazer_movimento(movimento, estado.copiar())
            if novoEstado:
                aval, _ = minimax(novoEstado, profundidade - 1, alfa, beta, False)
                if aval > maxAval:
                    maxAval = aval
                    melhorMovimento = movimento
                alfa = max(alfa, aval)
                if beta <= alfa:
                    break
        return maxAval, melhorMovimento
    else:
        minAval = float('inf')
        melhorMovimento = None
        for movimento in gerar_movimentos(estado):
            novoEstado = fazer_movimento(movimento, estado.copiar())
            if novoEstado:
                aval, _ = minimax(novoEstado, profundidade - 1, alfa, beta, True)
                if aval < minAval:
                    minAval = aval
                    melhorMovimento = movimento
                beta = min(beta, aval)
                if beta <= alfa:
                    break
        return minAval, melhorMovimento
