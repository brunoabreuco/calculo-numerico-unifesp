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

print("E.1 -----------------------")

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

print("E.2 -----------------------")

# Caso (i)
print("Caso (i) ------------")

# 1. Desempacota o resultado
root, history = kepler(0.10, 0.5)

# 2. Imprime a resposta com 6 casas decimais.
print(f"Anomalia excêntrica (E) = {root:.6f} rad")

# 3. Informa o número de iterações.
# O número de iterações é o tamanho da lista 'history'
print(f"Método convergiu em {len(history)} iterações.")


# Caso (ii)
print("Caso (ii) ------------")

# 1. Desempacota o resultado
root, history = kepler(0.90, 0.1)

# 2. Imprime a resposta com 6 casas decimais.
print(f"Anomalia excêntrica (E) = {root:.6f} rad")

# 3. Informa o número de iterações.
# O número de iterações é o tamanho da lista 'history'
print(f"Método convergiu em {len(history)} iterações.")


# Caso (iii)
print("Caso (iii) ------------")

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

print("E.3 -----------------------")

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

print("E.4 -----------------------")

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