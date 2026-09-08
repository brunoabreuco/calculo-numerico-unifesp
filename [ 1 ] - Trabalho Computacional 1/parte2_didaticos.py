import math
import pandas as pd
from metodos import *


print("\n" + "="*60)
print(" PARTE 2 — EXERCÍCIOS DIDÁTICOS")
print("="*60)

# =====================================================================================================
# Função-teste padrão desta parte do trabalho computacional.
def f(x):
    return x**3 - 9*x + 3

"""
Exercício 2.1 - Isolamento
"""
# Obs: A função tabelar_sinais() pedida neste exercício foi implementada 
# no arquivo metodos.py por se tratar de um algoritmo numérico reutilizável.

print("\n[2.1] Isolamento")
print("-" * 30)

# =====================================================================================================
# Letra A: Função f(x) = x^3 - 9x + 3
print("\n>> Letra (a): Função f(x) = x^3 - 9x + 3 no intervalo [-5, 5]")

print(f"{'n=21':<6} -> {tabelar_sinais(f, -5, 5, 21)}")
print(f"{'n=11':<6} -> {tabelar_sinais(f, -5, 5, 11)}")
print(f"{'n=6':<6}  -> {tabelar_sinais(f, -5, 5, 6)}")
print(f"{'n=4':<6}  -> {tabelar_sinais(f, -5, 5, 4)}")


# =====================================================================================================
# Letra B: Função f(x) = (x-1.05)(x-1.15)(x-3)
print("\n>> Letra (b): Função f(x) = (x-1.05)(x-1.15)(x-3) no intervalo [0, 4]")

def fb(x):
    return (x-1.05)*(x-1.15)*(x-3)

print(f"{'n=9':<6}   -> {tabelar_sinais(fb, 0, 4, 9)}")
print(f"{'n=17':<6}  -> {tabelar_sinais(fb, 0, 4, 17)}")
print(f"{'n=41':<6}  -> {tabelar_sinais(fb, 0, 4, 41)}")
print(f"{'n=401':<6} -> {tabelar_sinais(fb, 0, 4, 401)}")

"""
Análise:
As raízes de fb(x) são 1.05, 1.15 e 3.0.
Note que para n=9 e n=17, o método não encontrou as duas primeiras raízes (próximas de 1).
Isso ocorre porque o passo da malha era grande demais, fazendo a função passar por duas raízes muito próximas dentro do mesmo subintervalo, sem que o sinal nas pontas mudasse.
Apenas quando aumentamos os pontos para n=41 ou mais, o tamanho do passo ficou suficientemente pequeno 
para capturar a mudança de sinal individual de cada raiz!
"""

"""
Exercício 2.2 - Previsão x Realidade na Bissecção
"""
print("\n[2.2] Previsão x Realidade na Bissecção")
print("-" * 45)

# Lista de tolerâncias exigidas para a análise de desempenho.
epsilons = [10**-2, 10**-4, 10**-6, 10**-8, 10**-10]

dados_ex2_2 = []
# Para cada tolerância da lista, calculamos o número teórico de iterações 
# usando a fórmula matemática baseada em logaritmos, e comparamos com o 
# número de passos efetivos retornados pelo código real da bisseção.
for epsilon in epsilons:
    k_teorico = math.ceil((math.log(1) - math.log(epsilon)) / math.log(2))
    _, historic = bisseccao(f, 0, 1, eps=epsilon)
    k_efetivo = len(historic)
    dados_ex2_2.append({"Epsilon": epsilon, "k previsto (fórmula)": k_teorico, "k efetivo (bissecção)": k_efetivo})

# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_ex2_2 = pd.DataFrame(dados_ex2_2)
print(df_ex2_2.to_markdown(index=False))

"""
Análise:
O número de iterações teóricas (k previsto pela fórmula da bissecção) é exatemente igual ao número efetivo de iterações executadas pelo algoritmo.
Isso ocorre porque o método da bissecção reduz o tamanho do intervalo de busca estritamente pela metade a cada passo, de forma perfeitamente determinística, independentemente do "formato" da curva de f(x). 
Diferente dos métodos de Newton e Secante (que dependem das inclinações da função), a convergência da bissecção depende apenas do tamanho inicial do intervalo e da tolerância eps exigida!
"""

"""
Exercício 2.3 - Custo Real: Avaliação de Função
"""

print("\n[2.3] Custo Real: Avaliações de Função")
print("-" * 45)

# Derivada analítica f'(x) necessária para o Método de Newton.
def df(x):
    return 3*x**2 - 9

# Executa cada um dos três métodos numéricos para a tolerância padrão de eps = 1e-8,
# usando o decorator contador para capturar o número exato de chamadas à f e f'
f_biss = contador(f)
hist_biss = bisseccao(f_biss, 0, 1)[1]

f_newton = contador(f)
df_newton = contador(df)
hist_newton = newton(f_newton, df_newton, x0=0.5)[1]

f_sec = contador(f)
hist_secante = secante(f_sec, 0, 1)[1]

# Contagem de iterações através do comprimento da lista de histórico de cada método.
it_biss = len(hist_biss)
it_newton = len(hist_newton)
it_secante = len(hist_secante)

# Monta a tabela estruturada pegando as contagens reais gravadas no atributo .n do decorator
tabela_ex3 = [
    ["Bisseccao", it_biss, f_biss.n, 0],
    ["Newton", it_newton, f_newton.n, df_newton.n],
    ["Secante", it_secante, f_sec.n, 0]
]

# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_ex2_3 = pd.DataFrame(tabela_ex3, columns=["Metodo", "Iteracoes", "Avaliacoes de f", "Avaliacoes de f'"])
print(df_ex2_3.to_markdown(index=False))

"""
Análise:
Embora o Método de Newton exija o menor número de iterações (apenas 3), cada passo dele custa caro computacionalmente, pois exige avaliar tanto f(x) quanto f'(x). 
O Método da Secante tem um pouco mais de iterações (5), mas como não precisa calcular a derivada, o custo total de avaliações de função é idêntico ao de Newton (6 avaliações de f no total).
Já a Bissecção se mostra extremamente ineficiente nesse aspecto, demandando 27 avaliações de f para atingir a mesma tolerância.
"""

"""
Exercício 4 - Ordem Empírica de Convergência
"""
print("\n[2.4] Ordem Empírica de Convergência")
print("-" * 45)

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
    erros = [abs(item["x"] - xi) for item in hist]
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
dados_ex2_4_newton = [{"Iteracao (k)": it, "p_k empirico": round(pk, 4)} for it, pk in ordens_newton]
# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_ex2_4_newton = pd.DataFrame(dados_ex2_4_newton)
print(df_ex2_4_newton.to_markdown(index=False))

print("\nMETODO DA SECANTE (Teorico: p ~= 1.618)")
dados_ex2_4_secante = [{"Iteracao (k)": it, "p_k empirico": round(pk, 4)} for it, pk in ordens_secante]
# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_ex2_4_secante = pd.DataFrame(dados_ex2_4_secante)
print(df_ex2_4_secante.to_markdown(index=False))

"""
Análise:
Para o Método de Newton, a ordem empírica calculada na 3ª iteração é de 1.9988, próxima do valor teórico p=2.
Para o Método da Secante, a ordem varia um pouco nas primeiras iterações devido às aproximações iniciais, mas converge em direção à proporção áurea p ≈ 1.618, atingindo 1.7361 na 5ª iteração.
"""

"""
Exercício 2.5 - Os Modos de Falha de Newton
"""
print("\n[2.5] Os Modos de Falha de Newton")
print("-" * 40)

# Caso (a): Estudo de oscilação / ciclos infinitos.
# Define uma função onde o método de Newton entra em loop cíclico sem convergir,
# fixando estritamente em 10 iterações para observar a alternância dos valores.
def fa(x):
    return x**3 - 2*x + 2

def dfa(x):
    return 3*x**2 - 2

_, hist_a = newton(fa, dfa, x0=0, max_iter=10)

print("\n>> Caso (a): Oscilação")
dados_ex2_5a = [{"k": item['k'], "x": round(item['x'], 6)} for item in hist_a]
# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_ex2_5a = pd.DataFrame(dados_ex2_5a)
print(df_ex2_5a.to_markdown(index=False))


# Caso (b): Estudo de divergência por afastamento utilizando a função arctan(x).
def fb_caso(x):
    return math.atan(x)

def dfb_caso(x):
    return 1 / (1 + x**2)

print("\n>> Caso (b): Divergência (x0 = 2.0)")
try:
    # Testa chute inicial distante (além do raio de convergência segura), gerando estouro numérico.
    _, hist_b2 = newton(fb_caso, dfb_caso, x0=2.0, max_iter=10)

    for item in hist_b2[:5]:
        print(f"k={item['k']}, xk={item['x']:.4f}")

except Exception as e:
    print(f"Divergiu/Estourou com OverflowError: {e}")

print("\n>> Caso (b): Convergência (x0 = 1.0)")

try:
    # Testa chute próximo à raiz, demonstrando convergência bem-sucedida.
    _, hist_b1 = newton(fb_caso, dfb_caso, x0=1.0, max_iter=10)

    for item in hist_b1[:5]:
        print(f"k={item['k']}, xk={item['x']:.4f}")

except Exception as e:
    print(f"Erro: {e}")

print("\n>> Caso (b): Investigando Limite de x0")

# Realiza uma varredura ao redor da fronteira crítica para mapear o limiar de estabilidade.
for x_inicial in [1.39, 1.391, 1.40]:
    try:
        _, h = newton(fb_caso, dfb_caso, x0=x_inicial, max_iter=15)
        print(f"x0 = {x_inicial} convergiu em {len(h)} iteracoes (ultimo xk={h[-1]['x']:.4f})")

    except:
        print(f"x0 = {x_inicial} estourou/falhou por divergencia")


# Caso (c): Estudo de derivada nula no ponto inicial.
# Testa o método de Newton utilizando exatamente um chute onde a derivada se anula (f'(x0) = 0),
# resultando em reta tangente horizontal, divisão por zero ou divergência drástica.
def fc(x):
    return x**3 - 9*x + 3

def dfc(x):
    return 3*x**2 - 9

print("\n>> Caso (c): Derivada Nula (x0 = sqrt(3))")
try:
    res_c, hist_c = newton(fc, dfc, x0=math.sqrt(3), max_iter=5)
    print("Executou com sucesso, ultimo xk:", res_c)
except Exception as e:
    print(f"Ocorreu excecao esperada (derivada zero): {type(e).__name__}")

"""
Análise:
Caso (a): Oscilação - A tangente envia x_k de volta para o ponto anterior, prendendo o método em um ciclo infinito (0 -> 1 -> 0 -> 1).
Caso (b): Divergência - A função arctan(x) possui um raio de convergência restrito. Chutes dentro do limite (x0=1.0) convergem. Chutes fora (x0=2.0) lançam o próximo x_k para muito longe, divergindo para o infinito. Nossos testes empíricos limitaram essa fronteira entre 1.39 e 1.40.
Caso (c): Derivada Nula - Se f'(x0) = 0, a reta tangente é perfeitamente horizontal e nunca cruza o eixo x, causando uma divisão por zero matemática que quebra o algoritmo.
"""

"""
Exercício 2.6 - Raiz múltipla
"""
print("\n[2.6] Raiz Múltipla")
print("-" * 40)

# Função com raiz múltipla (m=2) no ponto x=2
def f_multipla(x):
    return (x - 2)**2 * (x + 1)

# Derivada analítica da função acima: f'(x) = 3x^2 - 6x
def df_multipla(x):
    return 3*x**2 - 6*x

print(">> Newton Tradicional (x0 = 3)")

# Executa Newton padrão a partir de x0=3 por 10 iterações fixas. Usando _ para ignorar a raiz final retornada, já que o que queremos aqui é o histórico.
_, hist_mult = newton(f_multipla, df_multipla, x0=3, max_iter=10)

# Extrai o erro absoluto ek = |x_k - 2.0| para todas as iterações
erros = [abs(item["x"] - 2.0) for item in hist_mult]

dados_ex2_6_trad = []
for i in range(len(hist_mult)):
    ek = erros[i]
    if i < len(hist_mult) - 1:
        ek_plus_1 = erros[i+1]
        razao = ek_plus_1 / ek if ek != 0 else 0
        dados_ex2_6_trad.append({"k": hist_mult[i]['k'], "Erro ek": f"{ek:.8e}", "ek+1 / ek": round(razao, 4)})
    else:
        dados_ex2_6_trad.append({"k": hist_mult[i]['k'], "Erro ek": f"{ek:.8e}", "ek+1 / ek": "-"})

# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_ex2_6_trad = pd.DataFrame(dados_ex2_6_trad)
print(df_ex2_6_trad.to_markdown(index=False))

# Obs: A função de Newton Modificado pedida neste exercício foi implementada no arquivo metodos.py 
# sob o nome 'newton_modificado', para manter todos os métodos no mesmo local.

print("\n>> Newton Modificado (m = 2, x0 = 3)")

# Novamente descartamos a raiz em '_' para focar no histórico do erro
_, hist_mod = newton_modificado(f_multipla, df_multipla, x0=3, m=2, max_iter=10)

dados_ex2_6_mod = [{"k": item['k'], "Erro ek": f"{abs(item['x'] - 2.0):.8e}"} for item in hist_mod]
# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_ex2_6_mod = pd.DataFrame(dados_ex2_6_mod)
print(df_ex2_6_mod.to_markdown(index=False))

"""
Análise:
No Newton tradicional, a convergência para raízes múltiplas (em x=2, multiplicidade m=2) cai de quadrática para linear. Isso é evidenciado pela razão e_{k+1}/e_k, que se aproxima assintoticamente de (m-1)/m = 0.5.
Porém, ao usar o Newton modificado multiplicando o passo pela multiplicidade 'm', a convergência quadrática é completamente restaurada e o erro desaba quase a zero logo nas primeiras iterações.
"""


"""
Exercício 2.7 - A armadilha do resíduo
"""
print("\n[2.7] A armadilha do resíduo")
print("-" * 40)

def f_res(x):
    return (x - 1)**10

print(">> f(1.1) e f(1.3)")
print(f"f(1.1) = {f_res(1.1):.4e}")
print(f"f(1.3) = {f_res(1.3):.4e}")

# Nossa bisseccao oficial possui o criterio: error < eps OR abs(f(xk_next)) < eps
# Como f(x) = (x-1)^10 é sempre positiva, f(a)*f(b) > 0, o que aciona nossa validação de segurança e levanta ValueError.
# Vamos encapsular em um bloco try-except para demonstrar formalmente na saída do programa
# que o método é matematicamente incapaz de iniciar neste cenário, para responder a questão.

print(">> Bissecção com parada padrão (|Passo| < eps OU |f(x)| < eps):")
try:
    _, hist_res_padrao = bisseccao(f_res, 0, 1.5, eps=1e-8)
    
    # Extrai a última raiz aproximada
    raiz_padrao = hist_res_padrao[-1]['x']
    
    print(f"Raiz obtida: {raiz_padrao:.8f}")

except ValueError:
    print("A bissecção oficial bloqueou a execução (ValueError) porque f(a)*f(b) >= 0.")

# Tenta rodar a bissecção modificada (que também respeita a trava de segurança)
try:
    _, hist_res_passo = bisseccao_apenas_passo(f_res, 0, 1.5, eps=1e-8)
    
    # Extrai a última raiz aproximada
    raiz_passo = hist_res_passo[-1]['x']
    
    # Calcula o erro em relação à raiz verdadeira x=1
    erro_passo = abs(raiz_passo - 1.0) 
    
    print("\n>> Bissecção com parada EXCLUSIVA de passo (|Passo| < eps):")
    print(f"Raiz obtida: {raiz_passo:.8f}")
    print(f"Erro real em x: {erro_passo:.8e}")
except ValueError:
    print("A bissecção modificada também foi bloqueada pela trava de sinal.")

"""
Análise:
Como f(x) = (x-1)^10 tem multiplicidade par, a função não cruza o eixo x (não há mudança de sinal).
Isso faz com que nossa Bissecção oficial trave imediatamente com ValueError, conforme a exigência do PDF.
Se a trava de segurança fosse desligada, o critério do resíduo seria extremamente perigoso: a função é tão "achatada" contra o eixo x que ela atinge a tolerância vertical |f(x)| < eps muito longe da raiz real, encerrando o algoritmo prematuramente com uma raiz falsa.
Esse critério só é adequado quando o usuário realmente se importa estritamente em zerar o processo físico que a função representa, sem se importar se a variável x em si está precisa.
"""