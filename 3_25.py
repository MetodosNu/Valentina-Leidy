"""
Examina la derivada de una función ruidosa (por ejemplo, al medir la velocidad de una partícula
en diferentes tiempos).
Como aún no hemos hablado de números aleatorios, modelaremos el efecto del ruido superponiendo un
comportamiento altamente oscilatorio en una función que varía lentamente. Para concretar, estudiemos:
f(x)= 2 + 5 sin(x) + 0.1 sin(30x)

El último término tiene una amplitud pequeña, pero contiene oscilaciones rápidas que tienen un gran
efecto en la derivada de la función. Toma 128 puntos igualmente espaciados en el intervalo de 0 a 2pi
y produce una tabla de valores (xi, f(xi)).

(a) Grafica f(x) con g(x), donde g(x) no contiene el término (el altamente oscilatorio). Observa que las
 dos curvas básicamente se superponen.

(b) Crea una gráfica que contenga: (i) la derivada analítica f'(x), (ii) la derivada analítica g'(x), y
 (iii) la aproximación de diferencia hacia adelante de f'(x), usando puntos adyacentes en tu malla. 
 Observa que tanto la derivada analítica f'(x) como la aproximación hacia adelante son altamente oscilatorias
 y, por lo tanto, muy diferentes del comportamiento “subyacente” de g'(x).

(c) Introduce un nuevo conjunto de puntos en tu última gráfica: (iv) la aproximación de diferencia hacia adelante
 de f'(x), usando una malla dos veces más gruesa (por ejemplo, para estimar la derivada en xi, usa los valores en
 x_(i+2) y xi. Observa que este conjunto de puntos exhibe “ruido” con amplitud más pequeña: esto se debe a que hemos
 duplicado el tamaño de paso h y, por lo tanto, suavizado algunas de las oscilaciones “no físicas” debidas al tercer
 término. (Las partes (b) y (c) emplean la aproximación de diferencia hacia adelante, es decir, no logramos una mejor
 aproximación de derivadas finitas de orden superior).
"""

import numpy as np
import matplotlib.pyplot as plt

# Definición de las funciones

# f(x) es la función "ruidosa": tiene un término de oscilación rápida (0.1*sin(30x))
def f(x):
    return 2 + 5 * np.sin(x) + 0.1 * np.sin(30 * x)

# g(x) es la función "suave": es la misma pero sin el término oscilatorio
def g(x):
    return 2 + 5 * np.sin(x)

# Derivadas analíticas

# f'(x): derivada exacta de f(x).
# - la derivada de 2 es 0
# - la derivada de 5sin(x) es 5cos(x)
# - la derivada de 0.1sin(30x) es 0.1*30cos(30x) = 3cos(30x)
def f_prime(x):
    return 5 * np.cos(x) + 3 * np.cos(30 * x)

# g'(x): derivada exacta de g(x).
# - solo queda la derivada de 5sin(x), que es 5cos(x)
def g_prime(x):
    return 5 * np.cos(x)

# Construcción de la malla de puntos

N = 128 # Número de puntos en la malla

# Se generan N puntos igualmente espaciados en el intervalo [0, 2π)
x = np.linspace(0, 2*np.pi, N, endpoint=False)

# El tamaño del paso h es la diferencia entre dos puntos consecutivos
h = x[1] - x[0]

# Parte (a): comparación de f(x) y g(x)

plt.figure(figsize=(10,5))
plt.plot(x, f(x), label="f(x) = 2 + 5sin(x) + 0.1sin(30x)")
plt.plot(x, g(x), '--', label="g(x) = 2 + 5sin(x)")
plt.title("Parte (a): Comparación entre f(x) y g(x)")
plt.xlabel("x")
plt.ylabel("Valor de la función")
plt.legend()
plt.grid()
plt.show()

# Parte (b): comparación de derivadas

# Aproximación de la derivada hacia adelante de f(x):
# forward_diff[i] ≈ ( f(x[i+1]) - f(x[i]) ) / h
# Se usa np.roll para "desplazar" el arreglo en 1 posición,
# de modo que f(x[i+1]) quede alineado con f(x[i])
forward_diff = (f(np.roll(x, -1)) - f(x)) / h

# Ajuste: el último valor no tiene vecino hacia adelante,
# así que copiamos el penúltimo valor para evitar errores
forward_diff[-1] = forward_diff[-2]

plt.figure(figsize=(10,5))
plt.plot(x, f_prime(x), label="f'(x) analítica")
plt.plot(x, g_prime(x), '--', label="g'(x) analítica")
plt.plot(x, forward_diff, ':', label="Aprox. diferencia hacia adelante de f'(x)")
plt.title("Parte (b): Comparación de derivadas")
plt.xlabel("x")
plt.ylabel("Valor de la derivada")
plt.legend()
plt.grid()
plt.show()

# Parte (c): derivada numérica con paso más grande

# Ahora calculamos con una malla "efectiva" más gruesa,
# usando un salto de 2h entre puntos.
# Fórmula: f'(x[i]) ≈ ( f(x[i+2]) - f(x[i]) ) / (2*h)
forward_diff_coarse = (f(np.roll(x, -2)) - f(x)) / (2*h)

# Ajuste: los dos últimos puntos no tienen vecinos a +2,
# así que les damos el mismo valor que el anterior.
forward_diff_coarse[-2:] = forward_diff_coarse[-3]

plt.figure(figsize=(10,5))
plt.plot(x, f_prime(x), label="f'(x) analítica")
plt.plot(x, g_prime(x), '--', label="g'(x) analítica")
plt.plot(x, forward_diff, ':', label="Aprox. paso h")
plt.plot(x, forward_diff_coarse, '-.', label="Aprox. paso 2h")
plt.title("Parte (c): Comparación con malla más gruesa")
plt.xlabel("x")
plt.ylabel("Valor de la derivada")
plt.legend()
plt.grid()
plt.show()
