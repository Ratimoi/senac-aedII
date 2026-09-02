# Implemente uma função que recebe uma string e retorna a mesma string com todas
# as vogais substituídas por ‘*’.

string = str(input("Insira uma palavra: "))
vogais = set("aeiou")

def trocaVogais(string):
    resultado = ""

    for i in string:
        for j in vogais:
            if i == j:
                i = '*'

        resultado += i

    return(resultado)

print(trocaVogais(string))
