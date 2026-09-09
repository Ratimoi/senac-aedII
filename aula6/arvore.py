valores = [10,5,2,7,15,12,20]

class Node():
    def __init__(self, valor):
        self.valor = valor
        self.esq = None
        self.dir = None

def inserir(raiz, valor):
    if raiz is None:
        return Node(valor)
    
    if valor < raiz.valor:
        raiz.esq = inserir(raiz.esq, valor)
    else:
        raiz.dir = inserir(raiz.dir, valor)

    return raiz

def imprimirPreOrdem(raiz):
    print(raiz.valor, end=" ")

    if raiz.esq is not None:
        imprimirPreOrdem(raiz.esq)

    if raiz.dir is not None:
        imprimirPreOrdem(raiz.dir)

def imprimirPosOrdem(raiz):
    if raiz.esq is not None:
        imprimirPosOrdem(raiz.esq)

    if raiz.dir is not None:
        imprimirPosOrdem(raiz.dir)

    print(raiz.valor, end=" ")

def imprimirOrdem(raiz):
    if raiz.esq is not None:
        imprimirOrdem(raiz.esq)

    print(raiz.valor, end=" ")

    if raiz.dir is not None:
        imprimirOrdem(raiz.dir)

tree = None

for valor in valores:
    tree = inserir(tree, valor)

print("Pre ordem: ")
imprimirPreOrdem(tree)
print()

print("Ordem: ")
imprimirOrdem(tree)
print()

print("Pos ordem: ")
imprimirPosOrdem(tree)
print()
