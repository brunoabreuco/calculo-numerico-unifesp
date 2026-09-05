#-------------------------
# exercicio 1
#-------------------------
print("Exercicio 1")
def f(x):
    return x**3 - 9*x + 3

def fb(x):
    return (x-1.05)*(x-1.15)*(x-3)


#todo: tratar zero
def sinal(atual, anterior):
    if(atual*anterior<0):
        return True
    else:
        return False


def tabelar_sinais (f, a, b , n):
    tamanhoPasso=abs(b-a)/(n-1)
    anterior=f(a)
    cordXanterior=a
    cordXatual = tamanhoPasso + a
    lista = []
    for i in range(n-1):
        atual=f(cordXatual)
        if(sinal(atual, anterior)):
            lista.append((cordXanterior,cordXatual))
        anterior=atual
        cordXatual+=tamanhoPasso
        cordXanterior+=tamanhoPasso
    print(lista)

tabelar_sinais(f, -5, 5, 21)
tabelar_sinais(f, -5, 5, 11)
tabelar_sinais(f, -5, 5, 6)
tabelar_sinais(f, -5, 5, 4)

tabelar_sinais(fb, 0, 4, 9)
tabelar_sinais(fb, 0, 4, 17)
tabelar_sinais(fb, 0, 4, 41)
tabelar_sinais(fb, 0, 4, 401)


#-------------------------
# exercicio 2
#-------------------------
print("\n\n")
print("Exercicio 2")

import math
from metodos import bisseccao, newton, secante


epsilons = [10**-2, 10**-4, 10**-6, 10**-8, 10**-10]

print("Epsilon       | k previsto (formula) | k efetivo (bisseccao)")
print("-" * 58)

for epsilon in epsilons:
    k_teorico = math.ceil((math.log(1) - math.log(epsilon)) / math.log(2))
    _, historic = bisseccao(f, 0, 1, eps=epsilon)
    k_efetivo = len(historic)
    
    print(f"{epsilon:<13} | {k_teorico:<20} | {k_efetivo}")


#-------------------------
# exercicio 3
#-------------------------
print("\n\n")
print("Exercicio 3")

from metodos import bisseccao, newton, secante

# Função de teste e sua derivada
def df(x):
    return 3*x**2 - 9

# Chamando os métodos (como 1e-8 já é o padrão de eps)
hist_biss = bisseccao(f, 0, 1)[1]
hist_newton = newton(f, df, x0=0.5)[1]
hist_secante = secante(f, 0, 1)[1]

# Contagem de iterações pelo tamanho do histórico
it_biss = len(hist_biss)
it_newton = len(hist_newton)
it_secante = len(hist_secante)

# Montando a tabela com base nas avaliações reais do código
tabela_ex3 = [
    ["Bisseccao", it_biss, it_biss, 0],
    ["Newton", it_newton, it_newton * 2, it_newton],
    ["Secante", it_secante, it_secante + 1, 0]
]

print(f"{'Metodo':<12} | {'Iteracoes':<10} | {'Avaliacoes de f':<16} | {'Avaliacoes de f\''}")
print("-" * 62)
for linha in tabela_ex3:
    print(f"{linha[0]:<12} | {linha[1]:<10} | {linha[2]:<16} | {linha[3]}")