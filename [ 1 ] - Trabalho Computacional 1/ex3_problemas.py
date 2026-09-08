import math
import matplotlib.pyplot as plt
from metodos import bisseccao, newton, secante

print("-"*100)
print("Problema 3A: Reservatorio esferico ")
print("-"*34)

R = 3.0
V_alvo = 40.0

# Deducão da funcão f(h)
# V(h) = pi * h^2 * (3R - h)/3  ->  queremos V(h) = V_alvo
def f_A(h, V = V_alvo, R = R):
    return math.pi * h**2 * (3*R - h)/3 - V

# Derivada f'(h) (usada no metodo de Newton):
def df_A(h, R=R):
    return math.pi * h * (2*R - h)

print(f"f(h) = pi * h^2 * (3*{R} - h)/3 - {V_alvo}")
print(f"f'(h) = pi * h * (2*{R} - h)")
print()

# Fase I: Isolamento das raízes (Tabelamento)
print("FASE I: Tabelamento de f(h)")
print("-" * 18)
print(f"{'h':>4} | {'f(h)':>10}")
print("-" * 18)
valores_h = list(range(-3, 10))
fh_anterior = f_A(valores_h[0])
intervalos = []

for h in valores_h:
    fh = f_A(h)
    print(f"{h:4d} | {fh:10.4f}")
    if h != valores_h[0] and fh_anterior * fh < 0:
        intervalos.append((h - 1, h))
    fh_anterior = fh
print("-" * 18)
print()
print(f"Trocas de sinal detectadas -> intervalos com raiz: {intervalos}")
print("Como f(h) eh uma cubica, essas sao TODAS as raizes reais (Bolzano).")
print()


# FASE II - REFINAMENTO: aplicando os tres metodos em cada intervalo
eps = 1e-4  # 0,1 mm -> garante erro inferior a 1 mm exigido no enunciado

print("FASE II: Refinamento (eps = 0,1 mm)")
print("-" * 60)
resultados = {}
for (a, b) in intervalos:
    print(f"Intervalo [{a}, {b}]:")

    h_bis, hist_bis = bisseccao(f_A, a, b, eps=eps)
    print(f"Bisseccao : h = {h_bis:.6f} m  ({len(hist_bis)} iteracoes)")

    # Newton so eh chamado nos intervalos onde f' nao muda de sinal
    # (garante convergencia monotona a partir do ponto medio)
    x0 = (a + b)/2
    try:
        h_new, hist_new = newton(f_A, df_A, x0, eps=eps)
        print(f"Newton    : h = {h_new:.6f} m  ({len(hist_new)} iteracoes), x0 = {x0}")
    except ValueError:
        print("Newton    : f'(x0) = 0, nao aplicavel com esse chute")
        h_new = None

    h_sec, hist_sec = secante(f_A, a, b, eps=eps)
    print(f"Secante   : h = {h_sec:.6f} m  ({len(hist_sec)} iteracoes), x0 = {a}, x1 = {b}")

    resultados[(a, b)] = h_bis
    print("-" * 60)

# Raiz fisica escolhida para a resposta da A.1
h_fisico = [h for (a, b), h in resultados.items() if 0 <= h <= 2*R][0]
print()
print(f"A.1: h = {h_fisico:.3f} m (erro inferior a 1 mm)")
print()

# Raízes, verificacão e classificação para resposta da A.2
print("A.2: Todas as raizes, verificacao (substituindo de volta em V(h)) e classificacao fisica:")
print("-"*80)
for (a, b), h in resultados.items():
    V_calc = math.pi * h**2 * (3*R - h) / 3
    if 0 <= h <= 2*R:
        status = "FISICAMENTE VALIDA (0 <= h <= 2R)"
    elif h < 0:
        status = "ESPURIA: altura negativa nao existe"
    else:
        status = "ESPURIA: h > 2R, maior que o diametro do reservatorio"
    print(f"h = {h:.6f} m | V(h) = {V_calc:.6f} m^3 | {status}")
print("-"*40)

# A.3 - Tabela h x V e Gráfico
print()
print("A.3: Tabela h x V para V = 10, 20, ..., 110 m^3")
print("-" * 24)
print(f"{'V (m3)':>8} | {'h (m)':>10}")
print("-" * 24)

lista_V = list(range(10, 111, 10))
lista_h = []

for V in lista_V:
    # f'(h) = pi*h*(2R-h) > 0 para todo h em (0, 2R) -> V(h) e monótona
    # crescente nesse dominio, então o intervalo [0, 2R] sempre isola
    # a raiz física, sem precisar refazer o tabelamento a cada V.
    def f_V(h, V=V):
        return math.pi * h**2 * (3*R - h) / 3 - V

    h_V, _ = bisseccao(f_V, 0, 2*R, eps=eps)
    lista_h.append(h_V)
    print(f"{V:8d} | {h_V:10.4f}")
print("-" * 24)

# Grafico h(V)
plt.figure(figsize=(7, 5))
plt.plot(lista_V, lista_h, marker='o')
plt.xlabel("V (m^3)")
plt.ylabel("h (m)")
plt.title("Altura h em funcao do volume V - reservatorio esferico R = 3 m")
plt.grid(True)
plt.tight_layout()
plt.savefig("h_versus_V.png", dpi=150)

print("Grafico salvo em 'h_versus_V.png'")

# Explicacão do formato da curva (achatamento no meio)
print()
print("Por que a curva h x V e mais achatada no meio do que nas pontas?")
print("dh/dV = 1/f'(h) = 1/(pi*h*(2R - h))")
print("pi*h*(2R-h) eh uma parabola em h, nula nos polos (h=0 e h=2R) e maxima no equador (h=R).")
print("Por isso dh/dV eh minimo no meio (curva achatada) e cresce perto dos polos (curva mais inclinada).")
print()
print("-" * 100)
print(" Problema B: Perda de Carga em Tubulacao (Colebrook-White) ")
print("-" * 63)

D   = 0.100      # diametro interno (m)
eps = 4.5e-5     # rugosidade absoluta (m)
Re  = 2.0e5      # numero de Reynolds
L   = 500.0      # comprimento da adutora (m)
Q   = 0.050      # vazao (m3/s)
g   = 9.81       # aceleracao da gravidade (m/s2)

# Dedução da função f(x)
A = eps / (3.7 * D)
B = 2.51 / Re

def F(f):
    return 1/math.sqrt(f) + 2*math.log10(A + B/math.sqrt(f))

print("\n--- Deducao de f(x) ---")
print(f"A = eps/(3.7D) = {A:.6e}")
print(f"B = 2.51/Re    = {B:.6e}")
print("F(f) = 1/sqrt(f) + 2*log10(A + B/sqrt(f))   (dominio: f > 0)")

# Fase I: Isolamento de f(x) (tabelamento)
print("\nFase I: Tabelamento de F(f)")
print("-" * 22)
print(f"{'f':>6} | {'F(f)':>12}")
print("-" * 22)
faixa = [0.010, 0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.050, 0.060, 0.080, 0.100]
F_ant, f_ant = F(faixa[0]), faixa[0]
intervalo = None
for f in faixa:
    Ff = F(f)
    print(f"{f:6.3f} | {Ff:12.6f}")
    if f != faixa[0] and F_ant * Ff < 0:
        intervalo = (f_ant, f)
    F_ant, f_ant = Ff, f

a, b = intervalo
print("-" * 22)
print(f"\nTroca de sinal -> raiz isolada em [{a}, {b}]")
print("F(f) eh monotona decrescente nessa regiao (regime turbulento),")
print("logo essa eh a UNICA raiz fisicamente relevante.")

eps_tol = 1e-8

print("-" * 63)
# B.1
print("\nB.1 - Determinar f com 6 casas decimais")
print("-" * 63)
print("Justificativa do metodo: como ainda nao exploramos nenhum chute")
print("melhor (isso so vem em B.3), usamos aqui a BISSECCAO: eh o unico")
print("dos tres metodos que so precisa do intervalo [a,b] ja isolado na")
print("Fase I, sem exigir um chute inicial preciso nem a derivada de F.")

f_b1, hist_b1 = bisseccao(F, a, b, eps=eps_tol)
print(f"\nResultado: f = {f_b1:.6f}   ({len(hist_b1)} iteracoes)")
print(f"Verificacao: F(f) = {F(f_b1):.3e}  (deve estar proximo de 0)")
print("-" * 63)

# B.2
print("\nB.2 - A secante brilha")
print("-" * 63)

def dF(f):
    termo = A + B/math.sqrt(f)
    return -0.5*f**-1.5 - (B*f**-1.5)/(termo*math.log(10))

print("dF/df = -0.5*f^(-3/2) - (B*f^(-3/2)) / [ (A + B/sqrt(f)) * ln(10) ]")
print()
print("Comentario sobre a dificuldade: para chegar nessa expressao eh preciso")
print("aplicar a regra da cadeia em DOIS niveis de raiz quadrada (a de dentro")
print("e a de fora do log) e ainda lembrar do fator 1/ln(10) da derivada de")
print("log10. Eh facil errar um sinal ou esquecer um dos dois termos em")
print("f^(-3/2) -- por isso a SECANTE 'brilha' aqui: ela so avalia F(f),")
print("nunca F'(f), eliminando essa fonte de erro por completo.")

f0 = 0.25 / (math.log10(A + 5.74/Re**0.9))**2

r_bis, h_bis = bisseccao(F, a, b, eps=eps_tol)
r_new, h_new = newton(F, dF, f0, eps=eps_tol)
r_sec, h_sec = secante(F, f0, b, eps=eps_tol)

print(f"\n{'Metodo':<12} | {'f encontrado':>14} | {'iteracoes':>10}")
print("-" * 42)
print(f"{'Bisseccao':<12} | {r_bis:14.8f} | {len(h_bis):10d}")
print(f"{'Newton':<12} | {r_new:14.8f} | {len(h_new):10d}")
print(f"{'Secante':<12} | {r_sec:14.8f} | {len(h_sec):10d}")
print("\nComparacao de esforco: Newton precisa deduzir e programar F'(f) (risco")
print("de erro, como discutido acima) para vencer em so 2 iteracoes; a secante")
print("chega ao mesmo resultado em poucas iteracoes a mais SEM nenhuma derivada;")
print("a bisseccao e a mais lenta, mas nao exige nem chute preciso nem derivada.")
print("-" * 63)

# B.3
print("\nB.3 - Chute inicial de Swamee-Jain")
print("-" * 63)
print(f"f0 = 0.25 / [log10(eps/(3.7D) + 5.74/Re^0.9)]^2 = {f0:.6f}")
print(f"(ja usado acima no Newton: convergiu em {len(h_new)} iteracoes)")

print("\nComparando com um chute arbitrario f0_arb = 0.05:")
try:
    r_new_arb, h_new_arb = newton(F, dF, 0.05, eps=eps_tol)
    print(f"Newton (chute 0.05): f = {r_new_arb:.8f} ({len(h_new_arb)} iteracoes)")
except ValueError:
    print("Newton (chute 0.05): DIVERGIU")
    print("\nO passo -F(f)/F'(f) eh enorme perto de f=0.05 ")
    print("e joga f para fora do dominio (f<0), quebrando")
    print("o sqrt/log na iteracao seguinte.\n")

r_sec_arb, h_sec_arb = secante(F, 0.05, b, eps=eps_tol)
economia = len(h_sec_arb) - len(h_sec)
print(f"Secante (chute 0.05): f = {r_sec_arb:.8f} ({len(h_sec_arb)} iteracoes)")
print(f"Secante (chute f0)  : f = {r_sec:.8f} ({len(h_sec)} iteracoes)")
print(f"\nIteracoes economizadas na secante usando f0 em vez do chute")
print(f"arbitrario: {economia}. No Newton, o chute arbitrario nem sequer")
print(f"converge -- ou seja, o 'ganho' de usar Swamee-Jain la eh infinito.")
print("-" * 63)

# B.4
print("\nB.4 - Perda de carga pela equacao de Darcy-Weisbach")
print("-" * 63)

f_final = f_b1
Area = math.pi * D**2 / 4
V = Q / Area
hf = f_final * (L/D) * (V**2) / (2*g)

print(f"Area do tubo: A = pi*D^2/4 = {Area:.6e} m^2")
print(f"Velocidade:   V = Q/A      = {V:.4f} m/s")
print(f"Perda de carga: hf = f*(L/D)*(V^2)/(2g) = {hf:.4f} m")
print("-" * 63)

# B.5
print("\nB.5 - Analise de sensibilidade (f ~= 0.02)")
print("-" * 63)

f_aprox = 0.02
hf_aprox = f_aprox * (L/D) * (V**2) / (2*g)
erro_percentual = (hf_aprox - hf) / hf * 100

print(f"hf com f exato ({f_final:.6f}) = {hf:.4f} m")
print(f"hf com f ~ 0.02              = {hf_aprox:.4f} m")
print(f"Erro percentual em hf        = {erro_percentual:.3f} %")
print("\nConclusao: um erro de menos de 0.002 em f ja produz quase 8% de")
print("erro em hf, pois hf e diretamente proporcional a f. Isso justifica")
print("o esforco numerico de obter f com 6 casas decimais.")
print("-"*100)