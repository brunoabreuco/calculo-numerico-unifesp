#-------------------------
# exercicio 1
#-------------------------
print("Exercicio 1 - Isolamento")

# Função-teste oficial do trabalho computacional.
def f(x):
    return x**3 - 9*x + 3

# Função auxiliar com raízes conhecidas próxima a 1 e 3.
def fb(x):
    return (x-1.05)*(x-1.15)*(x-3)

# Função auxiliar de sinal: verifica se houve mudança de sinal entre dois pontos consecutivos.
def sinal(atual, anterior):
    # Se o produto for menor ou igual a zero, há travessia de eixo ou raiz exata.
    if(atual*anterior<=0):
        return True
    else:
        return False

# Função de varredura (tabelamento de sinais): divide o intervalo [a, b] em 'n' pontos 
# para testar todos os subintervalos e encontrar quais deles contêm raízes.
def tabelar_sinais (f, a, b , n):
    # Cálculo do tamanho de cada passo da malha discreta.
    tamanhoPasso=abs(b-a)/(n-1)
    
    # Avaliação da função no extremo esquerdo inicial do intervalo.
    anterior=f(a)
    cordXanterior=a
    cordXatual = tamanhoPasso + a
    lista = []
    
    # Laço para percorrer todos os subintervalos gerados pela malha.
    for i in range(n-1):
        atual=f(cordXatual)
        
        # Verifica se o subintervalo contém uma raiz através da mudança de sinal.
        if(sinal(atual, anterior)):
            lista.append((cordXanterior,cordXatual))
            
        # Atualiza os valores e avança as coordenadas para o próximo passo.
        anterior=atual
        cordXatual+=tamanhoPasso
        cordXanterior+=tamanhoPasso
        
    print(lista)

print("\n funcao: x3-9x+3")
tabelar_sinais(f, -5, 5, 21)
tabelar_sinais(f, -5, 5, 11)
tabelar_sinais(f, -5, 5, 6)
tabelar_sinais(f, -5, 5, 4)

print("\n funcao: (x-1.05)(x-1.15)(x-3)")
tabelar_sinais(fb, 0, 4, 9)
tabelar_sinais(fb, 0, 4, 17)
tabelar_sinais(fb, 0, 4, 41)
tabelar_sinais(fb, 0, 4, 401)


#-------------------------
# exercicio 2
#-------------------------
print("\n\n")
print("Exercicio 2 - Previsao x realidade na bisseccao")

import math
from metodos import bisseccao, newton, secante

# Lista de tolerâncias exigidas para a análise de desempenho.
epsilons = [10**-2, 10**-4, 10**-6, 10**-8, 10**-10]

print("Epsilon       | k previsto (formula) | k efetivo (bisseccao)")
print("-" * 58)

# Para cada tolerância da lista, calculamos o número teórico de iterações 
# usando a fórmula matemática baseada em logaritmos, e comparamos com o 
# número de passos efetivos retornados pelo código real da bisseção.
for epsilon in epsilons:
    # Cálculo do teto do número de iterações teóricas.
    k_teorico = math.ceil((math.log(1) - math.log(epsilon)) / math.log(2))
    
    # Execução real do algoritmo da bisseção no intervalo [0, 1].
    _, historic = bisseccao(f, 0, 1, eps=epsilon)
    
    # O número efetivo corresponde ao tamanho da lista histórica gerada.
    k_efetivo = len(historic)
    
    print(f"{epsilon:<13} | {k_teorico:<20} | {k_efetivo}")


#-------------------------
# exercicio 3
#-------------------------
print("\n\n")
print("Exercicio 3 - Custo real: avaliacao de funcao")

from metodos import bisseccao, newton, secante

# Derivada analítica f'(x) necessária para o Método de Newton.
def df(x):
    return 3*x**2 - 9

# Executa cada um dos três métodos numéricos para a tolerância padrão de eps = 1e-8,
# capturando o histórico de execuções para quantificar o esforço computacional (custo).
hist_biss = bisseccao(f, 0, 1)[1]
hist_newton = newton(f, df, x0=0.5)[1]
hist_secante = secante(f, 0, 1)[1]

# Contagem de iterações através do comprimento da lista de histórico de cada método.
it_biss = len(hist_biss)
it_newton = len(hist_newton)
it_secante = len(hist_secante)

# Monta a tabela estruturada avaliando o número de chamadas de f e de derivadas f' 
# com base na arquitetura interna de cada algoritmo implementado.
tabela_ex3 = [
    ["Bisseccao", it_biss, it_biss, 0],
    ["Newton", it_newton, it_newton * 2, it_newton],
    ["Secante", it_secante, it_secante + 1, 0]
]

print(f"{'Metodo':<12} | {'Iteracoes':<10} | {'Avaliacoes de f':<16} | {'Avaliacoes de f\''}")
print("-" * 62)
for linha in tabela_ex3:
    print(f"{linha[0]:<12} | {linha[1]:<10} | {linha[2]:<16} | {linha[3]}")


#-------------------------
# exercicio 4
#-------------------------
print("\n\n")
print("Exercicio 4 - Ordem empirica de convergencia")

import math
from metodos import newton, secante

# Raiz exata fornecida para referência de cálculo do erro.
xi = 0.3376089559658377

# Execução dos métodos de Newton e Secante gerando os históricos de aproximações.
_, hist_newton = newton(f, df, x0=0.5)
_, hist_secante = secante(f, 0, 1)

# Função para calcular a ordem empírica de convergência (p_k):
# Utiliza três erros consecutivos (k-1, k, k+1) aplicados na fórmula logarítmica 
# para estimar a velocidade real com que o método converge para a raiz exata.
def calcular_ordem(hist, xi):
    # Mapeia cada aproximação xk do histórico no seu respectivo erro absoluto.
    erros = [abs(item["xk"] - xi) for item in hist]
    ordens = []
    
    # Percorre a partir da terceira posição para garantir a existência de três erros consecutivos.
    for i in range(2, len(erros)):
        ek_minus_1 = erros[i-2]
        ek = erros[i-1]
        ek_plus_1 = erros[i]
        
        # Interrompe o cálculo caso ocorra erro nulo para evitar divisão por zero.
        if ek_minus_1 == 0 or ek == 0 or ek_plus_1 == 0:
            break
            
        # Aplicação da fórmula empírica para estimar o expoente p_k.
        pk = math.log(ek_plus_1 / ek) / math.log(ek / ek_minus_1)
        ordens.append((i+1, pk))
        
    return ordens

ordens_newton = calcular_ordem(hist_newton, xi)
ordens_secante = calcular_ordem(hist_secante, xi)

print("METODO DE NEWTON (Teorico: p = 2)")
print(f"{'Iteracao (k)':<15} | {'p_k empirico':<15}")
print("-" * 35)
for it, pk in ordens_newton:
    print(f"{it:<15} | {pk:.4f}")

print("\nMETODO DA SECANTE (Teorico: p ~= 1.618)")
print(f"{'Iteracao (k)':<15} | {'p_k empirico':<15}")
print("-" * 35)
for it, pk in ordens_secante:
    print(f"{it:<15} | {pk:.4f}")


#-------------------------
# exercicio 5
#-------------------------
print("\n\n")
print("Exercicio 5 - Os modos de falha de Newton")

import math
from metodos import newton

# Caso (a): Estudo de oscilação / ciclos infinitos.
# Define uma função onde o método de Newton entra em loop cíclico sem convergir,
# fixando estritamente em 10 iterações para observar a alternância dos valores.
def fa(x):
    return x**3 - 2*x + 2

def dfa(x):
    return 3*x**2 - 2

_, hist_a = newton(fa, dfa, x0=0, max_iter=10)

print("\nCASO (a)")
print(f"{'k':<5} | {'xk':<15}")
print("-" * 25)
for item in hist_a:
    print(f"{item['k']:<5} | {item['xk']:.6f}")


# Caso (b): Estudo de divergência por afastamento utilizando a função arctan(x).
def fb_caso(x):
    return math.atan(x)

def dfb_caso(x):
    return 1 / (1 + x**2)

print("\nCASO (b): x0 = 2.0")
try:
    # Testa chute inicial distante (além do raio de convergência segura), gerando estouro numérico.
    _, hist_b2 = newton(fb_caso, dfb_caso, x0=2.0, max_iter=10)
    for item in hist_b2[:5]:
        print(f"k={item['k']}, xk={item['xk']:.4f}")
except Exception as e:
    print(f"Divergiu/Estourou com OverflowError: {e}")

print("\nCASO (b): x0 = 1.0")
try:
    # Testa chute próximo à raiz, demonstrando convergência bem-sucedida.
    _, hist_b1 = newton(fb_caso, dfb_caso, x0=1.0, max_iter=10)
    for item in hist_b1[:5]:
        print(f"k={item['k']}, xk={item['xk']:.4f}")
except Exception as e:
    print(f"Erro: {e}")

print("\nCASO (b): Investigando limite de x0")
# Realiza uma varredura ao redor da fronteira crítica para mapear o limiar de estabilidade.
for x_inicial in [1.39, 1.391, 1.40]:
    try:
        _, h = newton(fb_caso, dfb_caso, x0=x_inicial, max_iter=15)
        print(f"x0 = {x_inicial} convergiu em {len(h)} iteracoes (ultimo xk={h[-1]['xk']:.4f})")
    except:
        print(f"x0 = {x_inicial} estourou/falhou por divergencia")


# Caso (c): Estudo de derivada nula no ponto inicial.
# Testa o método de Newton utilizando exatamente um chute onde a derivada se anula (f'(x0) = 0),
# resultando em reta tangente horizontal, divisão por zero ou divergência drástica.
def fc(x):
    return x**3 - 9*x + 3

def dfc(x):
    return 3*x**2 - 9

print("\nCASO (c): x0 = sqrt(3)")
try:
    res_c, hist_c = newton(fc, dfc, x0=math.sqrt(3), max_iter=5)
    print("Executou com sucesso, ultimo xk:", res_c)
except Exception as e:
    print(f"Ocorreu excecao esperada (derivada zero): {type(e).__name__}")