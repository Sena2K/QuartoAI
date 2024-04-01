from tabuleiro import Tabuleiro
from quartoEnum import Quarto
from jogo import primitivo, minimax

if __name__ == "__main__":
    tabuleiro = Tabuleiro()
    while primitivo(tabuleiro) == Quarto.INDECISO:
        tabuleiro.imprimir_tabuleiro()
        if tabuleiro.jogador() == 1:
            print("Vez do Jogador 1 selecionar uma peça para o Jogador 2:")
            print(tabuleiro.get_nomes_pecas())
            indice_peca = int(input("Escolha um índice de peça: "))
            print(f"Você deu ao Jogador 2 a peça {tabuleiro.get_pecas()[indice_peca].get_nome_peca()}.")
            
            print("AI pensando...")
            _, movimento = minimax(tabuleiro, 2, float('-inf'), float('inf'), False)
            if movimento:
                _, linha, coluna = movimento
                tabuleiro.colocar_peca(indice_peca, linha, coluna)
                print(f"AI colocou a peça em ({linha}, {coluna})")
            else:
                print("AI não encontrou um movimento válido. Algo deu errado.")
        else:
            print("AI selecionando uma peça para o Jogador 1...")
            _, movimento = minimax(tabuleiro, 2, float('-inf'), float('inf'), True)
            if movimento:
                indice_peca = movimento[0]
                print(f"AI te dá a peça {tabuleiro.get_pecas()[indice_peca].get_nome_peca()}.")
                
                linha = int(input("Escolha a linha para colocar a peça: "))
                coluna = int(input("Escolha a coluna para colocar a peça: "))
                if not tabuleiro.colocar_peca(indice_peca, linha, coluna):
                    print("Movimento inválido, tente novamente.")
                    continue
            else:
                print("AI não encontrou um movimento válido. Algo deu errado.")

        if tabuleiro.verificar_vitoria():
            print("Fim de jogo.")
            tabuleiro.imprimir_tabuleiro()
            if tabuleiro.jogador() == 1:
                print("Você ganhou!")
            else:
                print("AI venceu!")
            break
        elif all(peca is None for peca in tabuleiro.get_pecas()):
            print("Fim de jogo.")
            print("Empate!")
            break
