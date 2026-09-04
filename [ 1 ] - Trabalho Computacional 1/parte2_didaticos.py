#-------------------------
# exercicio 1
#-------------------------
def f(x):
    return x**3 - 9*x + 3


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


#-------------------------
# exercicio 2
#-------------------------

import math

epsilons = [10**-2, 10**-4, 10**-6, 10**-8, 10**-10]

for epsilon in epsilons:
    k = (math.log(1) - math.log(epsilon)) / math.log(2)
    print(epsilon,"-", k)


#-------------------------
# exercicio 3
#-------------------------

        