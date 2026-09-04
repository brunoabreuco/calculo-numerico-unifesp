
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




        