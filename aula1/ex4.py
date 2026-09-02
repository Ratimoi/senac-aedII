# Implemente uma fila simples para processar uma sequência de nomes (entrada e
# saída), mostrando a fila a cada operação

fila = []

while True:
    print("1. Insira um nome")
    print("2. Próximo nome da fila")
    print("3. Sair")

    opcao = input("\nInsira uma opcao: ")

    match opcao:
        case '1':
            nome = input("\nInsira um nome: ")

            if nome:
                fila.append(nome)
            else:
                print("Nome vazio\n")

            print(f"Fila atual: {fila}\n")

        case '2':
            if fila:
                fila.pop(0)
            else:
                print("Fila está vazia\n")

            print(f"Fila atual: {fila}\n")
            
        case '3':
            break

        case _:
            print("Opção inválida\n")
