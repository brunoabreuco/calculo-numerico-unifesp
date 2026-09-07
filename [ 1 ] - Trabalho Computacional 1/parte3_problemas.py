import metodos
import math

"""
Problema E — Equação de Kepler
"""

# Definição da função kepler. Seja M a anomalia média e e a excentricidade da órbita. A função retornará E, que é a anomalia excêntrica.
def kepler(e,   M, E0=None):
    # Chute inicial do E.
    if E0 is None:
        E0 = M
    
    # Método de Newton aplicado à equação de Kepler. Retorna-se a raiz aproximada e o histórico de iterações.
    return metodos.newton(lambda E: E - e*math.sin(E) - M, lambda E: 1 - e*math.cos(E), E0)


# -----------------------------------------------------------------------------------------------------
# E.1 Para a órbita do cometa Halley, e = 0,967. Calcule E para M = 0,2 rad.

print("\n" + "="*60)
print(" PROBLEMA E — EQUAÇÃO DE KEPLER")
print("="*60)

print("\n[E.1] Órbita do Cometa Halley")
print("-" * 30)

print("Fase I (Tabelamento para isolamento da raiz):")
f_E = lambda E: E - 0.967*math.sin(E) - 0.2
for E_test in [0.0, 0.5, 1.0, 1.5]:
    print(f"f({E_test:.1f}) = {f_E(E_test):.4f}")
print("-> Mudança de sinal observada entre 1.0 e 1.5. Raiz isolada neste intervalo.\n")

# 1. Desempacota o resultado
root, history = kepler(0.967, 0.2)

# 2. Imprime a resposta
print(f"Anomalia excêntrica (E) = {root:.6f} rad")

# 3. Prova real (substituindo de volta na equação original)
M_calc = root - 0.967*math.sin(root)
print(f"Prova real: M calculado = {M_calc:.4f} (esperado: 0.2000)")

# 4. Informa o número de iterações.
print(f"Método convergiu em {len(history)} iterações.")

"""
Saída:

E.1 -----------------------
Anomalia excêntrica (E) = 1.028022 rad
Método convergiu em 6 iterações.
"""

# -----------------------------------------------------------------------------------------------------
# E.2 Resolva para os três casos descritos (i, ii, iii), usando Newton com chute inicial E0 = M:

print("\n[E.2] Robustez (Newton com E0 = M)")
print("-" * 35)

# Caso (i)
print("\n>> Caso (i): e = 0.10 | M = 0.5")

# 1. Desempacota o resultado
root, history = kepler(0.10, 0.5)

# 2. Imprime a resposta com 6 casas decimais.
print(f"Anomalia excêntrica (E) = {root:.6f} rad")

# 3. Informa o número de iterações.
# O número de iterações é o tamanho da lista 'history'
print(f"Método convergiu em {len(history)} iterações.")


# Caso (ii)
print("\n>> Caso (ii): e = 0.90 | M = 0.1")

# 1. Desempacota o resultado
root, history = kepler(0.90, 0.1)

# 2. Imprime a resposta com 6 casas decimais.
print(f"Anomalia excêntrica (E) = {root:.6f} rad")

# 3. Informa o número de iterações.
# O número de iterações é o tamanho da lista 'history'
print(f"Método convergiu em {len(history)} iterações.")


# Caso (iii)
print("\n>> Caso (iii): e = 0.99 | M = 0.01")

# 1. Desempacota o resultado
root, history = kepler(0.99, 0.01)

# 2. Imprime a resposta com 6 casas decimais.
print(f"Anomalia excêntrica (E) = {root:.6f} rad")

# 3. Informa o número de iterações.
# O número de iterações é o tamanho da lista 'history'
print(f"Método convergiu em {len(history)} iterações.")

"""
Saída:

E.2 -----------------------
Caso (i) ------------
Anomalia excêntrica (E) = 0.552480 rad
Método convergiu em 2 iterações.

Caso (ii) ------------
Anomalia excêntrica (E) = 0.630844 rad
Método convergiu em 5 iterações.

Caso (iii) ------------
Anomalia excêntrica (E) = 0.342270 rad
Método convergiu em 7 iterações.

Análise:
O esforço aumenta à medida que a excentricidade e se aproxima de 1. O motivo disso é que, como o chute inicial é próximo de zero (E ≈ 0) e o termo cos(E) se aproxima de 1, a derivada f'(E) = 1 - e*cos(E) se aproxima de zero. Isso faz com que o método de Newton (que divide por f'(E)) sofra com instabilidade inicial, dando passos exagerados que exigem mais iterações para corrigir.
"""

# -----------------------------------------------------------------------------------------------------
# E.3 Um chute inicial melhor para órbitas muito excêntricas é E0 = M + e sin M. Refaça o caso (iii) com ele e compare.

print("\n[E.3] Chute Inicial Melhorado para Órbitas Excêntricas")
print("-" * 55)

# 1. Desempacota o resultado
root, history = kepler(0.99, 0.01, 0.01 + 0.99*math.sin(0.01))

# 2. Imprime a resposta com 6 casas decimais.
print(f"Anomalia excêntrica (E) = {root:.6f} rad")

# 3. Informa o número de iterações.
# O número de iterações é o tamanho da lista 'history'
print(f"Método convergiu em {len(history)} iterações.")

"""
Saída:

E.3 -----------------------
Anomalia excêntrica (E) = 0.342270 rad
Método convergiu em 7 iterações.

Análise:
O novo chute inicial não melhorou o esforço computacional, já que o número de iterações foi o mesmo.
Embora o chute E0 = M + e*sin(M) seja teoricamente mais próximo da raiz verdadeira, neste caso extremo (e=0.99, M=0.01) ele não foi suficiente para reduzir o número de iterações. Isso ocorre porque o novo chute inicial ainda está na região crítica próxima a zero, onde a derivada é muito pequena. Logo, o método de Newton sofre do mesmo problema de instabilidade no primeiro passo em ambos os casos.
"""

# -----------------------------------------------------------------------------------------------------
# E.4 Para o caso (iii), rode também a bissecção em [0; π]. Ela converge? Em quantas iterações? Qual método você recomendaria para um software de rastreamento de satélites que precisa resolver essa equação milhões de vezes por segundo, e por quê?

print("\n[E.4] Comparação com a Bissecção")
print("-" * 35)

# 1. Desempacota o resultado
root, history = metodos.bisseccao(lambda E: E - 0.99*math.sin(E) - 0.01, 0, math.pi)

# 2. Imprime a resposta com 6 casas decimais.
print(f"Anomalia excêntrica (E) = {root:.6f} rad")

# 3. Informa o número de iterações.
# O número de iterações é o tamanho da lista 'history'
print(f"Método da Bissecção convergiu em {len(history)} iterações.")

"""
Saída:

E.4 -----------------------
Anomalia excêntrica (E) = 0.342270 rad
Método da Bissecção convergiu em 22 iterações.

Análise:
A função converge e encontra a mesma raiz nos outros casos, mas exige bem mais iterações para isso, 22 nesse caso. Para um software que precisa resolver essa equação milhões de vezes por segundo, recomendaria o método de Newton com um chute inicial inteligente. A vantagem é a velocidade (22 iterações contra 7), apesar da fragilidade do método em casos extremos.
"""

"""
Problema F - Deflexão de Viga
"""

print("\n" + "="*60)
print(" PROBLEMA F — DEFLEXÃO DE VIGA (BÔNUS)")
print("="*60)

# Constantes da viga
L = 600
E_mod = 50000
I = 30000
w0 = 2.5
C = w0 / (120 * L * E_mod * I)

# Função de deflexão y(x)
def y_x(x):
    return C * (-(x**5) + 2*(L**2)*(x**3) - (L**4)*x)

# Derivada analítica dy/dx
def dy_dx(x):
    return C * (-5*(x**4) + 6*(L**2)*(x**2) - L**4)

# -----------------------------------------------------------------------------------------------------
# F.1 O ponto de deflexão máxima é onde dy/dx = 0. Derive analiticamente e encontre esse ponto.

print("\n[F.1] Ponto de Deflexão Máxima")
print("-" * 30)

# Usando a bissecção no intervalo [0, 300] (metade da viga)
root_F1, hist_F1 = metodos.bisseccao(dy_dx, 0, 300)
print(f"Ponto de deflexão máxima (x) = {root_F1:.4f} cm")
print(f"Método convergiu em {len(hist_F1)} iterações.")

# -----------------------------------------------------------------------------------------------------
# F.2 Calcule a deflexão máxima em cm.

print("\n[F.2] Deflexão Máxima")
print("-" * 30)

max_deflection = y_x(root_F1)
print(f"Deflexão máxima y(x) = {max_deflection:.4f} cm")

# -----------------------------------------------------------------------------------------------------
# F.3 Armadilha proposital. Avalie dy/dx em x = 0 e em x = L.

print("\n[F.3] Armadilha Proposital")
print("-" * 30)

print(f"dy/dx em x=0: {dy_dx(0):.4e}")
print(f"dy/dx em x=L: {dy_dx(L):.4f}")

"""
Análise:
Avaliando a derivada, observamos que dy/dx em x=L é exatamente ZERO (além da raiz verdadeira que procuramos).
Se tentarmos aplicar a bissecção no intervalo [0, L], teremos f(0) * f(L) = (negativo) * (0) = 0.
A nossa implementação da bissecção (como exigido no PDF) levanta um ValueError se f(a)*f(b) >= 0.
Ou seja, o programa quebra e levanta um ERRO. A correção é não usar a viga inteira, mas sim um intervalo que isolem apenas a raiz verdadeira, como [0, 300] (metade da viga).
"""

# -----------------------------------------------------------------------------------------------------
# F.4 Refaça F.1 usando uma derivada numérica em vez de analítica

print("\n[F.4] Derivada Numérica vs Analítica")
print("-" * 40)

# Raiz exata analítica: x = L / sqrt(5)
x_exact = L / math.sqrt(5)

h_values = [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]
errors = []

for h in h_values:
    # Derivada numérica
    def dy_dx_num(x):
        return (y_x(x + h) - y_x(x - h)) / (2 * h)
    
    # Acha a raiz usando a derivada numérica
    root_num, _ = metodos.bisseccao(dy_dx_num, 0, 300)
    
    # Calcula o erro em relação à raiz exata
    error = abs(root_num - x_exact)
    errors.append(error)
    print(f"h = {h:.0e} | x_encontrado = {root_num:.6f} | erro = {error:.2e}")

"""
Análise:
À medida que h fica muito pequeno (como 10^-10), o computador precisa subtrair dois números quase idênticos no numerador da derivada numérica (y(x+h) - y(x-h)).
Isso causa um fenômeno do Cálculo Numérico chamado "Cancelamento Catastrófico", onde a precisão de ponto flutuante do computador é perdida, aumentando o erro ao invés de diminuí-lo.
"""