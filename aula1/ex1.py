# Escreva um algoritmo que, dado um número inteiro, retorna a quantidade de dígitos
# pares existentes nele.

num = int(input("Insira um número inteiro: "))
count = 0

while num > 0:
    digito = num % 10

    if digito % 2 == 0 and digito != 0:
        count += 1

    num = num // 10

print(f"Total de pares: {count}")
