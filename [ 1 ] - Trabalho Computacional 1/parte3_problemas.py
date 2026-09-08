import math
import pandas as pd
from metodos import *


"""
Problema A — Reservatório Esférico
"""

print("\n" + "="*60)
print(" PROBLEMA A — RESERVATÓRIO ESFÉRICO")
print("="*60)

# Define o raio do reservatório em metros
R = 3.0


# -----------------------------------------------------------------------------------------------------
# A.1 Determine a altura h para que o reservatório contenha 40 m3 de água, com erro inferior a 1 mm.

# Define o volume alvo em metros cúbicos
V_alvo = 40.0

# Dedução da função f(h). A equação do volume é V(h) = pi * h^2 * (3R - h)/3. Queremos V(h) = V_alvo, então f(h) = V(h) - V_alvo = 0
def f_A(h, V=V_alvo, R=R):
    # Retorna o valor de f(h) para a altura h informada
    return math.pi * h**2 * (3*R - h)/3 - V

# Derivada analítica f'(h), necessária para o método de Newton
def df_A(h, R=R):
    # Retorna o valor da derivada no ponto h
    return math.pi * h * (2*R - h)

print("\n[A.1] Altura para Volume = 40 m³")
print("-" * 30)

# Gera uma lista de valores inteiros de -3 até 9 para testar o sinal da função
valores_h = list(range(-3, 10))

# Calcula o valor de f(h) para o primeiro elemento da lista (h = -3)
fh_anterior = f_A(valores_h[0])

# Inicializa a lista vazia que irá armazenar os intervalos contendo as raízes
intervalos = []

# Itera sobre cada valor de h na lista de testes silenciosamente
for h in valores_h:
    # Calcula o valor da função para o h atual
    fh = f_A(h)

    # Verifica se não é o primeiro valor e se houve mudança de sinal em relação ao h anterior
    if h != valores_h[0] and fh_anterior * fh < 0:

        # Se houve mudança de sinal, adiciona a tupla com o intervalo na lista
        intervalos.append((h - 1, h))

    # Atualiza o valor anterior para a próxima iteração
    fh_anterior = fh

# Seleciona o único intervalo de Bolzano que faz sentido físico, ou seja, entre 0 e 2*R
intervalo_valido = [i for i in intervalos if i[0] >= 0 and i[1] <= 2*R][0]

# Desempacota o intervalo
a, b = intervalo_valido

# Define a tolerância para a precisão dos métodos numéricos (10^-4 metros = 0.1 mm)
eps = 1e-4

# Chama o método da bissecção e recebe a raiz e o histórico de iterações
h_bis, hist_bis = bisseccao(f_A, a, b, eps=eps)

# Imprime a resposta
print(f"Altura encontrada (h) = {h_bis:.3f} m (erro inferior a 1 mm)")
print(f"Método convergiu em {len(hist_bis)} iterações.")


# -----------------------------------------------------------------------------------------------------
# A.2 A equação resultante é uma cúbica. Encontre todas as três raízes reais. Duas delas não servem. Explique o que cada raiz espúria significa e qual restrição física as elimina.

print("\n[A.2] Classificação de Todas as Raízes (Bolzano)")
print("-" * 30)

# Itera sobre todas as três raízes calculadas
for (a_i, b_i) in intervalos:
    # Acha a raiz de cada intervalo
    h, _ = bisseccao(f_A, a_i, b_i, eps=eps)

    # Substitui o h encontrado na função de Volume para realizar a prova real
    V_calc = math.pi * h**2 * (3*R - h) / 3

    # Verifica se a raiz está dentro dos limites reais do reservatório
    if 0 <= h <= 2*R:
        # Atribui o status de raiz válida
        status = "FISICAMENTE VÁLIDA (dentro do tanque)"

    # Verifica se a raiz é uma altura negativa
    elif h < 0:
        # Atribui o status de raiz espúria (impossível fisicamente)
        status = "ESPÚRIA (altura negativa)"

    # Se não é negativa nem válida, a altura ultrapassou o diâmetro da esfera
    else:
        # Atribui o status de raiz espúria por extrapolar os limites físicos
        status = "ESPÚRIA (maior que o tanque)"

    # Imprime a análise completa daquela raiz
    print(f"h = {h:.6f} m | V(h) = {V_calc:.2f} m³ | {status}")


# -----------------------------------------------------------------------------------------------------
# A.3 Tabela relacionando altura h e volume V para V variando de 10 a 110 m³.

print("\n[A.3] Tabela de Altura x Volume (V de 10 a 110 m³)")
print("-" * 30)

# Cria a lista de volumes alvo espaçados de 10 em 10 m³
lista_V = list(range(10, 111, 10))
dados_a3 = []

# Itera sobre todos os volumes alvo desejados e imprime a tabela
for V in lista_V:
    # Função auxiliar redefinida a cada iteração encapsulando o volume alvo atual
    def f_V(h, V=V):
        # Retorna a expressão do volume para a altura desejada subtraída do alvo atual
        return math.pi * h**2 * (3*R - h) / 3 - V

    # Aplica a bissecção entre 0 e o diâmetro para achar a altura respectiva deste volume
    h_V, _ = bisseccao(f_V, 0, 2*R, eps=eps)

    dados_a3.append({"V (m3)": V, "h (m)": round(h_V, 4)})

# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_a3 = pd.DataFrame(dados_a3)
print(df_a3.to_markdown(index=False))

'''
Análise:
A relação entre h e V (como visto na tabela) demonstra que o enchimento é mais lento no meio porque a taxa de variação dh/dV = 1/f'(h) é inversamente proporcional a f'(h). Como a derivada f'(h) (área da superfície do líquido) atinge seu máximo no equador da esfera (h=R) e é zero nos polos, o nível sobe muito devagar no meio do tanque e rapidamente nas pontas.
'''

"""
Problema B — Perda de Carga em Tubulação
"""

print("\n" + "="*60)
print(" PROBLEMA B — PERDA DE CARGA EM TUBULAÇÃO")
print("="*60)

# Define o diâmetro interno da tubulação em metros
D   = 0.100      

# Define a rugosidade absoluta da tubulação em metros
eps_rug = 4.5e-5 

# Define o número de Reynolds
Re  = 2.0e5      

# Define o comprimento da adutora em metros
L   = 500.0    

# Define a vazão volumétrica (m³/s)
Q   = 0.050   

# Define a aceleração da gravidade (m/s²)
g   = 9.81       

# Calcula a constante A da equação de Colebrook-White
A = eps_rug / (3.7 * D)

# Calcula a constante B da equação de Colebrook-White
B = 2.51 / Re

# Função f(x) a ser zerada, isolando o fator de atrito 'f' na equação de Colebrook-White
def F(f):
    # Retorna o erro residual da equação para um determinado 'f' testado
    return 1/math.sqrt(f) + 2*math.log10(A + B/math.sqrt(f))

# Derivada analítica em relação a 'f', necessária para aplicar o método de Newton
def dF(f):
    # Calcula e armazena o termo do interior do logaritmo da derivada
    termo = A + B/math.sqrt(f)

    # Retorna o resultado final da regra da cadeia extensa de Colebrook-White
    return -0.5*f**-1.5 - (B*f**-1.5)/(termo*math.log(10))


# -----------------------------------------------------------------------------------------------------
# B.1 Determine f com 6 casas decimais.

print("\n[B.1] Fator de Atrito (f)")
print("-" * 30)

# Define uma série de valores de f (chutes razoáveis de rugosidade) para isolamento silencioso
faixa = [0.010, 0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.050, 0.060, 0.080, 0.100]

# Salva o valor inicial de F(f) para a primeira extremidade
F_ant, f_ant = F(faixa[0]), faixa[0]

# Inicia a variável do intervalo vazio
intervalo = None

# Itera sobre todos os chutes iniciais da faixa
for f in faixa:
    # Calcula F para o f atual
    Ff = F(f)

    # Detecta se ocorreu uma passagem pelo zero
    if f != faixa[0] and F_ant * Ff < 0:
        # Armazena as duas extremidades formadoras do isolamento da raiz
        intervalo = (f_ant, f)

    # Atualiza as variáveis de memória para o próximo passo do loop
    F_ant, f_ant = Ff, f

# Extrai os limites encontrados na tupla
a_B, b_B = intervalo

# Define a tolerância baixíssima de precisão numérica requerida no enunciado (1e-8)
eps_tol = 1e-8

# Aplica a bissecção para isolar o fator f até a tolerância fina estabelecida
f_b1, hist_b1 = bisseccao(F, a_B, b_B, eps=eps_tol)

# Imprime a raiz refinada na saída do terminal
print(f"f = {f_b1:.6f}")

# Imprime o total de iterações necessárias
print(f"Método da Bissecção convergiu em {len(hist_b1)} iterações.")


# -----------------------------------------------------------------------------------------------------
# B.2 e B.3 Compare o desempenho numérico (número de iterações) entre os métodos da Bissecção, Newton e Secante.

print("\n[B.2 e B.3] Comparação Numérica (Bissecção vs Newton vs Secante)")
print("-" * 45)

# Define f0 usando a fórmula empírica de Swamee-Jain que serve de chute inicial perfeito
f0 = 0.25 / (math.log10(A + 5.74/Re**0.9))**2

# Roda o método da bissecção e guarda resultados
r_bis, h_bis = bisseccao(F, a_B, b_B, eps=eps_tol)

# Roda o método de newton partindo do chute de Swamee-Jain
r_new, h_new = newton(F, dF, f0, eps=eps_tol)

# Roda o método da secante utilizando o chute empírico e a extremidade de Bolzano
r_sec, h_sec = secante(F, f0, b_B, eps=eps_tol)

dados_b23 = [
    {"Método": "Bisseccao", "f encontrado": f"{r_bis:.8f}", "iterações": len(h_bis)},
    {"Método": "Newton", "f encontrado": f"{r_new:.8f}", "iterações": len(h_new)},
    {"Método": "Secante", "f encontrado": f"{r_sec:.8f}", "iterações": len(h_sec)}
]
# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_b23 = pd.DataFrame(dados_b23)
print(df_b23.to_markdown(index=False))

'''
Análise:
A Secante "brilha" neste problema, pois chega ao resultado quase na mesma velocidade que Newton (4 vs 3 iterações), mas sem precisar do cálculo exato da derivada, que na equação de Colebrook-White é extensa, exigindo múltiplas regras da cadeia e acarretando alto risco de erro humano. O uso da aproximação de Swamee-Jain como chute inicial é fundamental: um chute arbitrário como 0.05 faz o método de Newton divergir devido à instabilidade logarítmica para raízes negativas.
'''


# -----------------------------------------------------------------------------------------------------
# B.4 e B.5 Calcule a perda de carga e realize a análise de sensibilidade do coeficiente de atrito.

print("\n[B.4 e B.5] Perda de Carga Final e Sensibilidade")
print("-" * 45)

# Calcula a área da tubulação (m²) para chegar na perda
Area = math.pi * D**2 / 4

# Calcula a velocidade vetorial linear da vazão
V = Q / Area

# Calcula a perda de carga Hf exata no sistema baseada no coeficiente descoberto pelo iterador numérico
hf = f_b1 * (L/D) * (V**2) / (2*g)

# Exibe a quantia exata de metros perdidos como restrição pra bomba
print(f"Perda de carga hf (exata) = {hf:.4f} m")

# Define o chute arbitrário irrealista para avaliar impactos em grande escala
f_aprox = 0.02

# Calcula a perda de carga incorreta que esse chute renderia 
hf_aprox = f_aprox * (L/D) * (V**2) / (2*g)

# Acha o erro relativo esticado (impacto logístico)
erro_percentual = (hf_aprox - hf) / hf * 100

'''
Análise B.5:
Ao chutar o valor de f = 0.02, a perda de carga sobe para hf = {hf_aprox:.4f} m, incorrendo em um erro de projeto de {erro_percentual:.2f}%.
Um desvio minúsculo na estimativa do coeficiente de atrito de 0.0195 para 0.020 gerou quase 3% de erro.
Como a perda de carga é diretamente proporcional ao fator 'f', imprecisões no fator são transferidas 1:1 para o cálculo estrutural de pressão e custo das bombas, justificando a precisão de 6 casas decimais e o esforço computacional das raízes.
'''


"""
Problema C - Equação de van der Waals
"""

# ============================================================
# PROBLEMA C — EQUAÇÃO DE VAN DER WAALS
# ============================================================
print("\n" + "="*60)
print(" PROBLEMA C — EQUAÇÃO DE VAN DER WAALS")
print("="*60)

# Constante universal dos gases (J/(mol K))
R = 8.314

# Constante 'a' de van der Waals para o CO2 (Pa m^6/mol^2)
a = 0.3640

# Constante 'b' de van der Waals para o CO2 (m^3/mol)
b = 4.267e-5

# Temperatura usada no problema (K)
T = 300.0

# Pressão inicial (Pa)
P = 5.0e6

# Função que calcula a equação polinomial de van der Waals para um volume v
def f_vdw(v, pressao=P):
    # Equação de van der Waals para v: P*v^3 - (P*b + R*T)*v^2 + a*v - a*b = 0
    return pressao * v**3 - (pressao * b + R * T) * v**2 + a * v - a * b

# -----------------------------------------------------------------------------------------------------
# C.1 Determine o volume molar v do gás ideal e usando a equação de van der Waals.

print("\n[C.1] Volume Molar (Gás Ideal vs Van der Waals)")
print("-" * 50)

# Volume pelo modelo de gás ideal
v_ideal = R * T / P

# Define o número de pontos para a busca logarítmica
n_pontos = 5000

# Define os expoentes inicial e final da malha logarítmica (10^-5 a 10^-2)
log_start, log_end = -5, -2

# Cria a malha de volumes espaçados logaritmicamente sem usar bibliotecas externas
pontos_v = [10**(log_start + i*(log_end - log_start)/(n_pontos-1)) for i in range(n_pontos)]

# Inicializa o armazenamento das raízes isoladas
intervalos_C1 = []

# Armazena o volume e o valor da função no ponto anterior para comparação
v_ant, f_ant = pontos_v[0], f_vdw(pontos_v[0])

# Itera sobre os pontos da malha para encontrar mudanças de sinal
for v_atual in pontos_v[1:]:
    # Calcula a função no ponto atual
    f_atual = f_vdw(v_atual)

    # Verifica se houve troca de sinal
    if f_ant * f_atual < 0:
        # Registra o intervalo que contém a raiz
        intervalos_C1.append((v_ant, v_atual))

    # Atualiza as variáveis para a próxima iteração
    v_ant, f_ant = v_atual, f_atual

# Pega os limites do primeiro (e único, neste caso) intervalo
a_c1, b_c1 = intervalos_C1[0]

# Define a tolerância fina para o volume (que tem ordem de grandeza 1e-4)
eps_c = 1e-12

# Aplica a bissecção para achar o volume molar de van der Waals
v_vdw, hist_c1 = bisseccao(lambda v: f_vdw(v, P), a_c1, b_c1, eps=eps_c)

# Calcula o erro percentual do gás ideal
erro_c1 = abs(v_ideal - v_vdw) / abs(v_vdw) * 100

# Imprime os resultados encontrados
print(f"Volume pelo gás ideal: {v_ideal:.6e} m³/mol")
print(f"Volume por van der Waals: {v_vdw:.6e} m³/mol")
print(f"Erro percentual do gás ideal: {erro_c1:.4f}%")
print(f"Método convergiu em {len(hist_c1)} iterações.")

# -----------------------------------------------------------------------------------------------------
# C.2 Verifique se há outras raízes na equação sob estas mesmas condições.

print("\n[C.2] Quantidade de Raízes (T = 300K, P = 5MPa)")
print("-" * 50)

# Imprime a quantidade de intervalos encontrados na mesma faixa
print(f"Quantidade de raízes encontradas entre 1e-5 e 1e-2 m³/mol: {len(intervalos_C1)}")

'''
Análise C.2 e C.3:
Abaixo da temperatura crítica, em certas pressões, a equação cúbica de van der Waals pode apresentar três raízes reais positivas. 
A menor raiz está associada à fase líquida, a maior à fase vapor, e a raiz intermediária corresponde a uma região instável do modelo. 
Neste caso específico de T=300K e P=5MPa, o tabelamento mostra apenas 1 raiz real positiva, indicando que o gás está em uma fase única.
O método numérico encontra a raiz pertencente ao intervalo isolado na Fase I, por isso é importante identificar todos os intervalos com mudança de sinal.
'''

# -----------------------------------------------------------------------------------------------------
# C.4 Gere as raízes (isoterma) para pressões variando de 1 a 10 MPa (passo 0.5 MPa).

print("\n[C.4] Isoterma P x v para T = 300 K")
print("-" * 50)

dados_c4 = []

# Define as pressões em MPa variando de 1.0 a 10.0 com passo de 0.5
pressoes_mpa = [1.0 + i*0.5 for i in range(19)]

# Itera sobre cada pressão para encontrar as raízes
for p_mpa in pressoes_mpa:
    # Converte a pressão para Pascal
    p_pa = p_mpa * 1e6

    # Define a função de van der Waals para a pressão específica
    f_p = lambda v, pressao=p_pa: f_vdw(v, pressao)
    
    # Reinicia a lista de intervalos para a nova pressão
    intervalos_P = []

    # Reseta as variáveis de memória do tabelamento
    v_ant, f_ant = pontos_v[0], f_p(pontos_v[0])
    
    # Itera sobre a malha de volumes logarítmica
    for v_atual in pontos_v[1:]:
        # Calcula a função no ponto atual
        f_atual = f_p(v_atual)

        # Verifica se houve troca de sinal
        if f_ant * f_atual < 0:
            # Salva o intervalo encontrado
            intervalos_P.append((v_ant, v_atual))

        # Atualiza a memória
        v_ant, f_ant = v_atual, f_atual
    
    # Prepara uma lista para as raízes desta pressão
    raizes_P = []

    # Itera sobre os intervalos encontrados
    for a_p, b_p in intervalos_P:
        # Encontra a raiz por bissecção
        raiz_p, _ = bisseccao(f_p, a_p, b_p, eps=eps_c)

        # Adiciona a raiz refinada à lista
        raizes_P.append(raiz_p)
    
    # Formata e imprime as raízes encontradas
    raizes_str = " | ".join([f"{r:.6e}" for r in raizes_P])
    dados_c4.append({"P (MPa)": p_mpa, "Raízes de van der Waals (m³/mol)": raizes_str})

# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_c4 = pd.DataFrame(dados_c4)
print(df_c4.to_markdown(index=False))


"""
Problema D - Taxa Interna de Retorno
"""

# ============================================================
# PROBLEMA D — TAXA INTERNA DE RETORNO (TIR)
# ============================================================
print("\n" + "="*60)
print(" PROBLEMA D — TAXA INTERNA DE RETORNO (TIR)")
print("="*60)

# Fluxos de caixa do projeto 1 (em mil reais)
fluxos_D1 = [-1000.0, 300.0, 350.0, 400.0, 450.0]

# Função para calcular o Valor Presente Líquido (VPL)
def vpl(taxa, fluxos):
    # Soma os fluxos trazidos a valor presente
    return sum([fluxo / (1.0 + taxa)**ano for ano, fluxo in enumerate(fluxos)])

# -----------------------------------------------------------------------------------------------------
# D.1 Calcule a TIR do projeto.

print("\n[D.1] Cálculo da TIR")
print("-" * 30)

# Cria malha de taxas i (0 a 50%) para o tabelamento
n_taxas = 100

# Gera a lista de taxas com passo igual sem usar linspace
taxas_i = [0.0 + i*(0.5)/n_taxas for i in range(n_taxas + 1)]

# Inicializa as variáveis do tabelamento
i_ant, vpl_ant = taxas_i[0], vpl(taxas_i[0], fluxos_D1)

# Variável para armazenar o intervalo da TIR
intervalo_tir = None

# Procura a raiz no intervalo [0, 0.5]
for i_atual in taxas_i[1:]:
    # Calcula o VPL atual
    vpl_atual = vpl(i_atual, fluxos_D1)

    # Checa mudança de sinal
    if vpl_ant * vpl_atual < 0:
        # Salva as extremidades
        intervalo_tir = (i_ant, i_atual)

    # Atualiza memória
    i_ant, vpl_ant = i_atual, vpl_atual

# Desempacota os limites
a_d, b_d = intervalo_tir

# Define a precisão da TIR
eps_d = 1e-6

# Aplica a bissecção
tir_1, hist_d1 = bisseccao(lambda i: vpl(i, fluxos_D1), a_d, b_d, eps=eps_d)

# Imprime os resultados
print(f"TIR encontrada = {tir_1:.6f} ({tir_1*100:.4f}% ao ano)")
print(f"VPL(TIR) calculado = {vpl(tir_1, fluxos_D1):.6e} mil R$")
print(f"Método convergiu em {len(hist_d1)} iterações.")

# -----------------------------------------------------------------------------------------------------
# D.2 Tabela do VPL (Substitui o Gráfico devido a restrição)

print("\n[D.2] Tabela VPL x Taxa (0% a 50%)")
print("-" * 30)

# Gera taxas de 0% a 50% de 5 em 5%
taxas_tabela = [i/100 for i in range(0, 55, 5)]
dados_d2 = []
# Itera e imprime
for t in taxas_tabela:
    dados_d2.append({"Taxa (%)": t*100, "VPL (mil R$)": round(vpl(t, fluxos_D1), 2)})

# Gera a tabela pelo pandas e imprime em formato markdown no terminal
df_d2 = pd.DataFrame(dados_d2)
print(df_d2.to_markdown(index=False))

# -----------------------------------------------------------------------------------------------------
# D.3 Tome a decisão para custos de capital de 15% e 20%.

print("\n[D.3] Decisão para custos de capital (15% e 20%)")
print("-" * 50)

# Calcula o VPL para 15%
vpl_15 = vpl(0.15, fluxos_D1)

# Calcula o VPL para 20%
vpl_20 = vpl(0.20, fluxos_D1)

# Imprime a decisão para 15%
print(f"VPL a 15% = {vpl_15:6.2f} mil R$ -> {'ACEITAR' if vpl_15 > 0 else 'REJEITAR'} o projeto.")

# Imprime a decisão para 20%
print(f"VPL a 20% = {vpl_20:6.2f} mil R$ -> {'ACEITAR' if vpl_20 > 0 else 'REJEITAR'} o projeto.")

# -----------------------------------------------------------------------------------------------------
# D.4 Projeto com múltiplas TIRs (-1000, 2500, -1540).

print("\n[D.4] Projeto com Múltiplas TIRs")
print("-" * 40)

# Fluxos do projeto 2
fluxos_D2 = [-1000.0, 2500.0, -1540.0]

# Gera malha de taxas (0 a 80%) para achar todas as TIRs (777 passos para evitar acerto exato na raiz)
taxas_d2 = [0.0 + i*(0.8)/777 for i in range(778)]

# Variáveis do tabelamento
i_ant, vpl_ant = taxas_d2[0], vpl(taxas_d2[0], fluxos_D2)

# Cria lista de intervalos vazia
intervalos_d4 = []

# Busca as mudanças de sinal
for i_atual in taxas_d2[1:]:
    # Calcula VPL
    vpl_atual = vpl(i_atual, fluxos_D2)
    
    # Checa inversão
    if vpl_ant * vpl_atual < 0:
        # Adiciona a raiz isolada
        intervalos_d4.append((i_ant, i_atual))

    # Atualiza variáveis
    i_ant, vpl_ant = i_atual, vpl_atual

# Itera sobre os intervalos encontrados
for idx, (a_d4, b_d4) in enumerate(intervalos_d4, start=1):
    # Aplica bissecção
    tir_2, hist_d4 = bisseccao(lambda i: vpl(i, fluxos_D2), a_d4, b_d4, eps=eps_d)

    # Imprime a TIR achada
    print(f"TIR {idx} = {tir_2*100:.4f}% ({len(hist_d4)} iterações)")

'''
Análise D.4:
Se Newton fosse executado com apenas um chute inicial arbitrário, ele poderia convergir para somente uma das duas TIRs ou divergir completamente. 
O analista poderia então concluir incorretamente que existe uma única taxa interna de retorno e tomar decisões erradas. 
A Fase I (tabelamento) é essencial neste caso porque permite visualizar e isolar TODAS as raízes antes da aplicação do refinamento numérico, evitando os perigos de funções não-monotônicas.
'''


"""
Problema E - Equação de Kepler
"""

print("\n" + "="*60)
print(" PROBLEMA E — EQUAÇÃO DE KEPLER")
print("="*60)

# Função encapsulada para resolver a Equação de Kepler
def kepler(e, M, E0=None, eps=1e-8):
    # Se não houver chute inicial fornecido, usa a aproximação de que E0 = M (válido para excentricidades pequenas)
    if E0 is None:
        E0 = M
    
    # f(E) = E - e*sen(E) - M
    f_E = lambda E: E - e * math.sin(E) - M
    # f'(E) = 1 - e*cos(E)
    df_E = lambda E: 1 - e * math.cos(E)
    
    # Chama o método de Newton com tolerância padrão (10^-8)
    return newton(f_E, df_E, E0, eps=eps)

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
Análise:
O novo chute inicial não melhorou o esforço computacional, já que o número de iterações foi o mesmo.
Embora o chute E0 = M + e*sin(M) seja teoricamente mais próximo da raiz verdadeira, neste caso extremo (e=0.99, M=0.01) ele não foi suficiente para reduzir o número de iterações. Isso ocorre porque o novo chute inicial ainda está na região crítica próxima a zero, onde a derivada é muito pequena. Logo, o método de Newton sofre do mesmo problema de instabilidade no primeiro passo em ambos os casos.
"""

# -----------------------------------------------------------------------------------------------------
# E.4 Para o caso (iii), rode também a bissecção em [0; π]. Ela converge? Em quantas iterações? Qual método você recomendaria para um software de rastreamento de satélites que precisa resolver essa equação milhões de vezes por segundo, e por quê?

print("\n[E.4] Comparação com a Bissecção")
print("-" * 35)

# 1. Desempacota o resultado
root, history = bisseccao(lambda E: E - 0.99*math.sin(E) - 0.01, 0, math.pi, eps=1e-8)

# 2. Imprime a resposta com 6 casas decimais.
print(f"Anomalia excêntrica (E) = {root:.6f} rad")

# 3. Informa o número de iterações.
print(f"Método da Bissecção convergiu em {len(history)} iterações.")

last_step = history[-1]
print(f"Erro final (passo): {last_step['erro']:.2e} | |f(x)| final: {abs(last_step['fx']):.2e}")
if abs(last_step['fx']) < 1e-8 and last_step['erro'] >= 1e-8:
    print("AVISO: A bissecção parou pelo critério de resíduo (|f(x)| < eps) antes do passo atingir a tolerância nominal. Precisão real do passo: ~7.5e-7.")

"""
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
root_F1, hist_F1 = bisseccao(dy_dx, 0, 300)
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
    # Derivada numérica avaliada diretamente na raiz exata
    deriv_num = (y_x(x_exact + h) - y_x(x_exact - h)) / (2 * h)
    
    # Calcula o erro em relação à derivada analítica na raiz exata (que é zero, mas fazemos a diferença)
    error = abs(deriv_num - dy_dx(x_exact))
    errors.append(error)
    print(f"h = {h:.0e} | dy_dx_num = {deriv_num:.6e} | erro = {error:.2e}")

"""
Análise:
À medida que h fica muito pequeno (como 10^-10), o computador precisa subtrair dois números quase idênticos no numerador da derivada numérica (y(x+h) - y(x-h)).
Isso causa um fenômeno do Cálculo Numérico chamado "Cancelamento Catastrófico", onde a precisão de ponto flutuante do computador é perdida, aumentando o erro ao invés de diminuí-lo.
"""