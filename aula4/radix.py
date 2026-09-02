import threading
import time
import multiprocessing
import heapq

ARQUIVO_CSV = "numeros_100M_embaralhado.csv"


def carregar_vetor(caminho=ARQUIVO_CSV):
    vetor = []

    with open(caminho, "r") as f:
        for linha in f:
            valor_limpo = linha.strip()

            if valor_limpo.isdigit():
                vetor.append(int(valor_limpo))

    return vetor


def maiorNumero(vetor):
    maior = vetor[0]
    for i in range(1, len(vetor)):
        if vetor[i] > maior:
            maior = vetor[i]

    return maior


def esta_ordenado_crescente(vetor):
    for i in range(1, len(vetor)):
        if vetor[i] < vetor[i - 1]:
            return False

    return True


def esta_ordenado_decrescente(vetor):
    for i in range(1, len(vetor)):
        if int(vetor[i]) > int(vetor[i - 1]):
            return False

    return True


#################################################################################################
# Versão 1 - recursiva, filtrando dígito a dígito, com uma thread nova em CADA nível de recursão.
# Cada nível faz 10 varreduras completas (uma por dígito) em vez de 1, e o numero de threads pode
# explodir se PROFUNDIDADE_MAX_THREADS for alto -> é a mais lenta e a mais arriscada das quatro.
# Ordena em ordem DECRESCENTE (efeito colateral do jeito que os baldes são concatenados).
#################################################################################################

PROFUNDIDADE_MAX_THREADS = 3


def formatar(vetor):
    maior = len(str(maiorNumero(vetor)))
    for i in range(len(vetor)):
        vetor[i] = str(vetor[i]).zfill(maior)

    return vetor


def radix_recursivo_threads(vetor, index, algarismo, profundidade_threads=PROFUNDIDADE_MAX_THREADS):
    v = []
    for i in range(len(vetor)):
        if str(vetor[i])[index] == str(algarismo):
            v.append(vetor[i])

    if len(v) <= 1:
        return v

    if index + 1 >= len(v[0]):
        return v

    if profundidade_threads > 0:
        resultados = [None] * 10

        def worker(digito):
            resultados[digito] = radix_recursivo_threads(v, index + 1, digito, profundidade_threads - 1)

        threads = [threading.Thread(target=worker, args=(digito,)) for digito in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()
    else:
        resultados = [radix_recursivo_threads(v, index + 1, digito, 0) for digito in range(10)]

    v0, v1, v2, v3, v4, v5, v6, v7, v8, v9 = resultados

    return v9 + v8 + v7 + v6 + v5 + v4 + v3 + v2 + v1 + v0


def ordenar_recursivo_threads(vetor):
    vetor = formatar(list(vetor))

    resultados = [None] * 10

    def worker(digito):
        resultados[digito] = radix_recursivo_threads(vetor, 0, digito, PROFUNDIDADE_MAX_THREADS - 1)

    threads = [threading.Thread(target=worker, args=(digito,)) for digito in range(10)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    v0, v1, v2, v3, v4, v5, v6, v7, v8, v9 = resultados

    return v9 + v8 + v7 + v6 + v5 + v4 + v3 + v2 + v1 + v0


#################################################################################################
# Versão 2 - iterativa com baldes (counting sort por dígito), SEM paralelismo.
# Uma única varredura por dígito, sem recursão nem cópias repetidas -> é a base de comparação.
# Ordena em ordem crescente e trabalha direto com inteiros (sem formatar/zfill).
#################################################################################################

def radix_rapido(vetor):
    if not vetor:
        return vetor

    maior = maiorNumero(vetor)
    qtd_digitos = len(str(maior))

    for posicao in range(qtd_digitos):
        baldes = [[] for _ in range(10)]
        divisor = 10 ** posicao

        for numero in vetor:
            digito = (numero // divisor) % 10
            baldes[digito].append(numero)

        vetor = [numero for balde in baldes for numero in balde]

    return vetor


#################################################################################################
# Versão 3 - iterativa com baldes, dividindo cada passada em pedaços contados por threads.
# O GIL do CPython impede paralelismo real em trabalho de CPU, então essa versão normalmente
# fica igual ou PIOR que a versão 2: serve para demonstrar o limite do GIL, não para acelerar.
#################################################################################################

NUM_THREADS_RAPIDO = 4


def radix_rapido_threads(vetor, num_threads=NUM_THREADS_RAPIDO):
    if not vetor:
        return vetor

    maior = maiorNumero(vetor)
    qtd_digitos = len(str(maior))

    tamanho_pedaco = max(1, len(vetor) // num_threads)
    pedacos = [vetor[i:i + tamanho_pedaco] for i in range(0, len(vetor), tamanho_pedaco)]

    for posicao in range(qtd_digitos):
        divisor = 10 ** posicao
        baldes_por_pedaco = [None] * len(pedacos)

        def contar(indice_pedaco):
            baldes = [[] for _ in range(10)]
            for numero in pedacos[indice_pedaco]:
                digito = (numero // divisor) % 10
                baldes[digito].append(numero)
            baldes_por_pedaco[indice_pedaco] = baldes

        threads = [threading.Thread(target=contar, args=(i,)) for i in range(len(pedacos))]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        vetor = [
            numero
            for digito in range(10)
            for baldes in baldes_por_pedaco
            for numero in baldes[digito]
        ]

        pedacos = [vetor[i:i + tamanho_pedaco] for i in range(0, len(vetor), tamanho_pedaco)]

    return vetor


#################################################################################################
# Versão 4 - divide o vetor em blocos grandes e ordena cada bloco em um PROCESSO separado
# (multiprocessing = paralelismo real, sem GIL), depois faz o merge final dos blocos já
# ordenados. Só compensa para vetores grandes (LIMIAR_PARALELO); abaixo disso, cai para a
# versão 2 sequencial, já que criar processos e serializar dados tem um custo fixo alto.
#################################################################################################

LIMIAR_PARALELO = 100_000
NUM_PROCESSOS = 4


def _ordenar_bloco(bloco):
    return radix_rapido(bloco)


def radix_rapido_processos(vetor, num_processos=NUM_PROCESSOS, limiar=LIMIAR_PARALELO):
    if len(vetor) < limiar:
        return radix_rapido(vetor)

    tamanho_bloco = max(1, len(vetor) // num_processos)
    blocos = [vetor[i:i + tamanho_bloco] for i in range(0, len(vetor), tamanho_bloco)]

    with multiprocessing.Pool(processes=num_processos) as pool:
        blocos_ordenados = pool.map(_ordenar_bloco, blocos)

    return list(heapq.merge(*blocos_ordenados))


#################################################################################################
# Execução e comparação das quatro versões
#################################################################################################

def executar(nome, funcao_ordenar, vetor, checar_ordenado):
    inicio = time.time()
    resultado = funcao_ordenar(list(vetor))
    fim = time.time()

    print(f"{nome}: {fim - inicio:.4f}s | ordenado corretamente: {checar_ordenado(resultado)}")


if __name__ == "__main__":
    vetor = carregar_vetor()

    executar("1) recursivo + thread por nivel  ", ordenar_recursivo_threads, vetor, esta_ordenado_decrescente)
    executar("2) baldes sequencial             ", radix_rapido, vetor, esta_ordenado_crescente)
    executar("3) baldes + threads por pedaco   ", radix_rapido_threads, vetor, esta_ordenado_crescente)
    executar("4) baldes + processos em blocos  ", radix_rapido_processos, vetor, esta_ordenado_crescente)
