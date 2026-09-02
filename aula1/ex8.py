# Crie um dicionário com nome (chave) e telefone (valor). Implemente funções para
# buscar telefone pelo nome e listar os contatos em ordem alfabética.

dicionario = {}

while True:
    print("1. Insira um contato")
    print("2. Listar contatos (ordem alfabética)")
    print("0. Sair")

    opcao = input("\nInsira uma opção: ")

    match opcao:
        case '1':
            print()

            nome = input("Insira um nome: ")
            telefone = input("Insira um telefone: ")

            dicionario[nome] = telefone

            print()

        case '2':
            print()

            for nome in sorted(dicionario):
                print(f"{nome}: {dicionario[nome]}")

            print()

        case '0':
            break

        case _:
            print("\nOpção inválida\n")

