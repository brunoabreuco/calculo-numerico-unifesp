import math
import matplotlib.pyplot as plt
from metodos import bisseccao, newton, secante

print(" PROBLEMA 3A: Reservatório Esférico ")
print("==================================================")
R = 3.0
V_target = 40.0

# Função deduzida: f(h) = h^3 - 9h^2 + 120/pi = 0
def f_A(h):
    return h**3 - 9 * h**2 + (3 * V_target) / math.pi

def df_A(h):
    return 3 * h**2 - 18 * h

