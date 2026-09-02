from pprint import pprint
from itertools import product

lista = ["ler", "escrever", "apagar"]

def gerarCombinacoes(lista):
    dicionario = {}
    combinacoesTotais = pow(2, len(lista)) - 1
    temp = combinacoesTotais
    i = 0

    while i <= combinacoesTotais:
        listaTupla = []
        j = 0

        while j < len(lista):
            binario = format(temp, '0' + str(len(lista)) + 'b')
            tupla = (lista[j], bool(int(binario[j])))
            listaTupla.append(tupla)

            j += 1

        dicionario.update({i:listaTupla})

        temp -= 1
        i += 1

    return dicionario

def gerarCombinacoesChat(lista):
    return [list(zip(lista, bits)) for bits in product([True, False], repeat=len(lista))]

pprint(gerarCombinacoes(lista))
pprint(gerarCombinacoesChat(lista))
