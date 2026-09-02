# Dado um vetor/lista de inteiros, escreva um algoritmo que retorna uma nova lista
# apenas com os números não-negativos

lista = [-3, 4, -1, 12, -2, 0]

def naoNegativos(lista):
    resultado = []

    for i in lista:
        if i > 0:
            resultado.append(i)

    return resultado

print(naoNegativos(lista))
