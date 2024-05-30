from collections import defaultdict
from tabuleiro import Tabuleiro, avaliar_estado, tabuleiro_para_estado, estado_para_tabuleiro
from quarto import Quarto
from tabuleiro import Tabuleiro, avaliar_estado
import random
import pickle

def jogar_contra_ia(Q):
    tabuleiro = Tabuleiro()
    jogador_atual = 1  # 1 para humano, 2 para IA

    while avaliar_estado(tabuleiro) == Quarto.INDECISO:
        print("Tabuleiro Atual:")
        tabuleiro.imprimir_tabuleiro()

        pecas_disponiveis = [(i, peca.get_nome_peca()) for i, peca in enumerate(tabuleiro.get_pecas()) if peca]
        print("Peças disponíveis para escolher:")
        for idx, nome in pecas_disponiveis:
            print(f"{idx}: {nome}")

        if jogador_atual == 1:
            indice_peca = None
            while indice_peca is None:
                try:
                    indice_peca = int(input("Escolha a peça para a IA jogar: "))
                    if not (0 <= indice_peca < len(tabuleiro.get_pecas()) and tabuleiro.get_pecas()[indice_peca]):
                        print("Peça inválida ou já escolhida, tente novamente.")
                        indice_peca = None
                except ValueError:
                    print("Entrada inválida, por favor insira um número.")

            acao = escolher_acao(tabuleiro, Q, epsilon=0.05)
            if acao:
                _, linha, coluna = acao
                if tabuleiro.colocar_peca(indice_peca, linha, coluna):
                    jogador_atual = 2
                else:
                    print("IA não conseguiu colocar a peça, verifique o erro.")
        else:
            acao = escolher_acao(tabuleiro, Q, epsilon=0.1)
            if acao:
                indice_peca, _, _ = acao
                print(f"A IA escolheu que você deve jogar com a peça: {tabuleiro.get_pecas()[indice_peca].get_nome_peca()}")

                movimento = None
                while movimento is None:
                    try:
                        print("Escolha onde colocar a peça (linha, coluna):")
                        entrada = input().split(',')
                        linha, coluna = map(int, entrada)
                        if tabuleiro.colocar_peca(indice_peca, linha, coluna):
                            movimento = True
                            jogador_atual = 1
                        else:
                            print("Movimento inválido, tente novamente.")
                            movimento = None
                    except Exception as e:
                        print("Entrada inválida, tente novamente.")

        if avaliar_estado(tabuleiro) != Quarto.INDECISO:
            print("Resultado final:")
            tabuleiro.imprimir_tabuleiro()
            print(f"{avaliar_estado(tabuleiro).name}")
            break

def assistir_jogo_ia(Q):
    tabuleiro = Tabuleiro()
    turno = 0
    while avaliar_estado(tabuleiro) == Quarto.INDECISO:
        ia_escolhe_peca = "IA1" if turno % 2 == 0 else "IA2"
        ia_joga = "IA2" if turno % 2 == 0 else "IA1"

        indice_peca = escolher_peca(tabuleiro, Q)
        if indice_peca is None:
            print(f"Nenhuma peça válida disponível, jogo encerrado.")
            break

        nome_peca = tabuleiro.pecas[indice_peca].get_nome_peca()
        print(f"{ia_escolhe_peca} escolheu a peça '{nome_peca}' para {ia_joga}.")

        acao = escolher_posicao(tabuleiro, Q, indice_peca)
        if acao is None:
            print(f"Nenhuma posição válida disponível, jogo encerrado.")
            break

        linha, coluna = acao
        tabuleiro.colocar_peca(indice_peca, linha, coluna)
        tabuleiro.imprimir_tabuleiro()

        estado_jogo = avaliar_estado(tabuleiro)
        if estado_jogo != Quarto.INDECISO:
            print(f"Resultado final: {estado_jogo.name}, vencedor: {ia_joga}")
            break

        turno += 1
        import time
        time.sleep(0.5)

def escolher_peca(tabuleiro, Q):
    pecas_disponiveis = [i for i, peca in enumerate(tabuleiro.get_pecas()) if peca]
    if not pecas_disponiveis:
        return None
    return random.choice(pecas_disponiveis)

def escolher_posicao(tabuleiro, Q, indice_peca):
    posicoes_possiveis = []
    for linha in range(tabuleiro.qtd_linhas):
        for coluna in range(tabuleiro.qtd_colunas):
            if tabuleiro.get_tabuleiro()[linha][coluna] is None:
                posicoes_possiveis.append((linha, coluna))

    if not posicoes_possiveis:
        return None

    return random.choice(posicoes_possiveis)


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

def recompensa(estado, acao, novo_estado):
    resultado = avaliar_estado(estado)
    novo_resultado = avaliar_estado(novo_estado)

    if novo_resultado == Quarto.VITORIA:
        return 1.0  # Grande recompensa por vencer
    elif novo_resultado == Quarto.DERROTA:
        return -1.0  # Grande penalidade por perder
    elif novo_resultado == Quarto.EMPATE:   
        return 0.5  # Recompensa intermediária por empatar

    incremento = 0
    if bloqueou_adversario(estado, acao):
        incremento += 0.3  # Recompensa por bloquear uma vitória do adversário
    if criou_oportunidade_vitoria(estado, acao):
        incremento += 0.4  # Recompensa por criar uma oportunidade de vitória
    if colocou_em_desvantagem(estado, acao):
        incremento -= 0.2  # Penalidade por colocar-se em desvantagem

    heuristica_novo_estado = avaliar_heuristica(novo_estado)
    incremento += heuristica_novo_estado * 0.01

    return incremento


def escolher_acao(tabuleiro, Q, epsilon=0.1):
    estado_atual = tabuleiro_para_estado(tabuleiro)
    acoes_possiveis = gerar_movimentos(tabuleiro)
    if not acoes_possiveis:
        return None

    if random.random() < epsilon:
        acao = random.choice(acoes_possiveis)
        print(f"Escolha aleatória: {acao}")
        return acao

    q_values = {acao: Q[estado_atual][acao] for acao in acoes_possiveis}
    max_q_value = max(q_values.values(), default=0)
    melhores_acoes = [acao for acao, q in q_values.items() if q == max_q_value]
    acao = random.choice(melhores_acoes)
    print(f"Valores Q: {q_values}, Escolha: {acao}")
    return acao


def atualizar_q(Q, estado, acao, recompensa, novo_estado, alpha, gamma):
    if novo_estado not in Q:
        Q[novo_estado] = defaultdict(float)
    max_q_novo = max(Q[novo_estado].values(), default=0)
    Q[estado][acao] += alpha * (recompensa + gamma * max_q_novo - Q[estado][acao])

def salvar_q(Q, filename='tabela_q.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(dict((k, dict(v)) for k, v in Q.items()), f)

def carregar_q(filename='tabela_q.pkl'):
    try:
        with open(filename, 'rb') as f:
            loaded_Q = pickle.load(f)
            return defaultdict(lambda: defaultdict(float), loaded_Q)
    except FileNotFoundError:
        return defaultdict(lambda: defaultdict(float))

def bloqueou_adversario(estado, acao):
    _, linha, coluna = acao
    peca_original = estado.tabuleiro[linha][coluna]
    estado.tabuleiro[linha][coluna] = None

    if estado.verificar_vitoria():
        estado.tabuleiro[linha][coluna] = peca_original
        return True

    estado.tabuleiro[linha][coluna] = peca_original
    return False

def criou_oportunidade_vitoria(estado, acao):
    _, linha_acao, coluna_acao = acao
    linhas_relevantes = [estado.tabuleiro[linha_acao]]
    colunas_relevantes = [[estado.tabuleiro[i][coluna_acao] for i in range(estado.qtd_linhas)]]

    diagonais_relevantes = []
    if linha_acao == coluna_acao:
        diagonais_relevantes.append([estado.tabuleiro[i][i] for i in range(estado.qtd_linhas)])
    if linha_acao + coluna_acao == estado.qtd_linhas - 1:
        diagonais_relevantes.append([estado.tabuleiro[i][estado.qtd_linhas - 1 - i] for i in range(estado.qtd_linhas)])

    todas_linhas = linhas_relevantes + colunas_relevantes + diagonais_relevantes
    for linha in todas_linhas:
        if linha.count(None) == 1 and linha.count(estado.pecas[0]) == 3:
            return True
    return False

def colocou_em_desvantagem(estado, acao):
    _, linha, coluna = acao
    peca_original = estado.tabuleiro[linha][coluna]
    estado.tabuleiro[linha][coluna] = None

    em_desvantagem = False
    for i in range(estado.qtd_linhas):
        for j in range(estado.qtd_colunas):
            if estado.tabuleiro[i][j] is None:
                estado.tabuleiro[i][j] = peca_original
                if estado.verificar_vitoria():
                    em_desvantagem = True
                estado.tabuleiro[i][j] = None
                if em_desvantagem:
                    break
        if em_desvantagem:
            break

    estado.tabuleiro[linha][coluna] = peca_original
    return em_desvantagem

def avaliar_heuristica(estado):
    pontuacao = 0
    for linha in estado.get_linhas():
        pontuacao += avaliar_linha(linha)
    for coluna in estado.get_colunas():
        pontuacao += avaliar_linha(coluna)
    diagonais = [
        [estado.tabuleiro[i][i] for i in range(estado.qtd_linhas)],
        [estado.tabuleiro[i][estado.qtd_linhas - 1 - i] for i in range(estado.qtd_linhas)]
    ]
    for diagonal in diagonais:
        pontuacao += avaliar_linha(diagonal)
    return pontuacao

def avaliar_linha(linha):
    if not linha or all(peca is None for peca in linha):
        return 0
    atributos_comuns = 0b1111
    for peca in linha:
        if peca:
            atributos_comuns &= peca.get_atributos()
    if atributos_comuns != 0:
        return 10
    return 0

def minimax(estado, profundidade, alfa, beta, maximizando_jogador):
    if profundidade == 0 or avaliar_estado(estado) != Quarto.INDECISO:
        return avaliar_heuristica(estado), None

    if maximizando_jogador:
        max_eval = float('-inf')
        melhor_movimento = None
        for movimento in gerar_movimentos(estado):
            novo_estado = fazer_movimento(movimento, estado.copiar())
            if novo_estado:
                eval, _ = minimax(novo_estado, profundidade - 1, alfa, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    melhor_movimento = movimento
                alfa = max(alfa, eval)
                if beta <= alfa:
                    break
        return max_eval, melhor_movimento
    else:
        min_eval = float('inf')
        melhor_movimento = None
        for movimento in gerar_movimentos(estado):
            novo_estado = fazer_movimento(movimento, estado.copiar())
            if novo_estado:
                eval, _ = minimax(novo_estado, profundidade - 1, alfa, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    melhor_movimento = movimento
                beta = min(beta, eval)
                if beta <= alfa:
                    break
        return min_eval, melhor_movimento

def treinar_ia(num_partidas, alpha=0.5, gamma=0.9, epsilon=0.01, epsilon_decay=0.999):
    Q = carregar_q()
    vitorias = 0

    for partida in range(num_partidas):
        tabuleiro = Tabuleiro()
        vitoria_flag = False

        while avaliar_estado(tabuleiro) == Quarto.INDECISO:
            acao = escolher_acao(tabuleiro, Q, epsilon)
            novo_tabuleiro = fazer_movimento(acao, tabuleiro.copiar())
            if not novo_tabuleiro:
                continue

            estado_novo = tabuleiro_para_estado(novo_tabuleiro)
            resultado = recompensa(tabuleiro, acao, novo_tabuleiro)
            atualizar_q(Q, tabuleiro_para_estado(tabuleiro), acao, resultado, estado_novo, alpha, gamma)

            tabuleiro = novo_tabuleiro

        if avaliar_estado(tabuleiro) == Quarto.VITORIA:
            vitorias += 1
            vitoria_flag = True

        epsilon *= epsilon_decay

        # Print progress every 10 games
        if partida % 10 == 0:
            print(f"Partida {partida}/{num_partidas}: Epsilon {epsilon:.10f}, Taxa de Vitória: {vitorias / (partida + 1) * 100:.2f}%, Vitoria nesta partida: {vitoria_flag}")

    return Q


def debug_print(Q, tabuleiro, estado_especifico):
    estado_atual = tabuleiro_para_estado(tabuleiro)
    if estado_atual == estado_especifico:
        print("Valores Q para estado específico:", Q[estado_especifico])
