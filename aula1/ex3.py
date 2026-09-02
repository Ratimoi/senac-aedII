# Usando a estrutura de pilha, crie uma função que inverta uma palavra digitada pelo
# usuário.

string = input("Insira uma palavra: ")

def inverterPalavra(string):
    lista = []

    for caracter in string:
        lista.append(caracter)

    inversa = ""

    while lista:
        inversa += lista.pop()

    return inversa

print(inverterPalavra(string))
