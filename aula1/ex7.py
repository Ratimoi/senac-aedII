# Dada uma frase, escreva um algoritmo que conte quantas vezes cada palavra
# aparece, retornando um dicionário com o resultado

frase = "um dois dois tres tres tres"

def contadorDicionario(frase):
    dicionario = {}

    partes = frase.split(' ')

    for palavra in partes:
        dicionario[palavra] = dicionario.get(palavra, 0) + 1

    return dicionario

print(f"Dicionario: {contadorDicionario(frase)}")
