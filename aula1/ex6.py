# Implemente uma função que recebe uma lista de números e retorna uma nova lista
# sem elementos repetidos, usando conjuntos (set).

lista = [2, 4, 1, 3, 2, 4, 1, 2]

def removeDuplicatas(lista):
    return list(set(lista))

print(removeDuplicatas(lista))
