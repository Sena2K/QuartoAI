from ia import treinar_ia, jogar_contra_ia, assistir_jogo_ia, carregar_q, salvar_q

def main():
    Q = carregar_q()
    while True:
        print("\nEscolha uma opção:")
        print("1 - Treinar o modelo")
        print("2 - Jogar contra a IA")
        print("3 - Ver um jogo de IA contra IA")
        print("4 - Sair")

        escolha = input("Digite sua opção: ")

        if escolha == '1':
            num_partidas = int(input("Digite o número de partidas para treinar: "))
            Q = treinar_ia(num_partidas)
            salvar_q(Q, 'tabela_q.pkl')
            print("Treinamento concluído e modelo salvo.")
        elif escolha == '2':
            jogar_contra_ia(Q)
        elif escolha == '3':
            assistir_jogo_ia(Q)
        elif escolha == '4':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
