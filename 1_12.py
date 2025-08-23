import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from copy import deepcopy
"""
FUNCIÓN: makefield(xs, ys)
Calcula el campo eléctrico generado por un conjunto de cargas
puntuales en una malla bidimensional definida por xs y ys.

Argumentos:
xs : lista/array con las coordenadas en el eje x
ys : lista/array con las coordenadas en el eje y

Retorna:
  Exs   : matriz 2D con la componente x del campo eléctrico
  Eys   : matriz 2D con la componente y del campo eléctrico
  qtopos: diccionario con las posiciones de las cargas
"""
def makefield(xs, ys):
    # Definición de las posiciones de las cargas.
    # En este caso: 4 cargas positivas ubicadas en los vértices
    # de un cuadrado centrado en el origen.
    qtopos = {
        +1: (-1, -1),   # carga en la esquina inferior izquierda
        +2: (1, -1),    # carga en la esquina inferior derecha
        +3: (-1, 1),    # carga en la esquina superior izquierda
        +4: (1, 1)      # carga en la esquina superior derecha
    }

    n = len(xs)  # número de puntos en cada dirección

    # Inicializamos matrices para las componentes del campo
    Exs = [[0. for k in range(n)] for j in range(n)]
    Eys = deepcopy(Exs)  # copia con las mismas dimensiones

    # Recorremos cada punto de la malla
    for j, x in enumerate(xs):
        for k, y in enumerate(ys):
            # Para cada carga, sumamos su contribución al campo
            for _, pos in qtopos.items():
                posx, posy = pos
                # Distancia desde la carga hasta el punto (x,y)
                R = sqrt((x - posx)**2 + (y - posy)**2)

                # Evitar división por cero cuando R ≈ 0
                if R < 1e-9:
                    continue

                # Campo eléctrico de una carga puntual:
                # E = k * q * (r - r0) / |r - r0|^3
                # Aquí tomamos k*q = 1 para simplificar.
                Exs[k][j] += (x - posx) / R**3
                Eys[k][j] += (y - posy) / R**3

    return Exs, Eys, qtopos


# FUNCIÓN: plotfield(boxl, n)

# Dibuja el campo eléctrico en una región cuadrada de tamaño 2*boxl.
#
# Argumentos:
#   boxl : semilado del área a graficar (ej. boxl=2 → área -2..2)
#   n    : número de puntos en la malla por cada eje

def plotfield(boxl, n):
    # Definimos la malla uniforme de puntos en el rango [-boxl, boxl]
    xs = [-boxl + i*2*boxl/(n-1) for i in range(n)]
    ys = xs[:]  # cuadrícula cuadrada

    # Calculamos el campo eléctrico en cada punto de la malla
    Exs, Eys, qtopos = makefield(xs, ys)

    # Convertimos listas a arrays de numpy para facilidad
    xs = np.array(xs)
    ys = np.array(ys)
    Exs = np.array(Exs)
    Eys = np.array(Eys)

    # Magnitud del campo eléctrico
    E = np.sqrt(Exs**2 + Eys**2)

    # Definir grosor de línea en función de la magnitud del campo
    # Usamos logaritmo para evitar valores demasiado grandes cerca de cargas
    lw = 0.8 * np.log1p(E)

    #  GRAFICAR LÍNEAS DE CAMPO 
    plt.figure(figsize=(6, 6))
    plt.streamplot(xs, ys, Exs, Eys,
                   density=1.5,      # densidad de líneas
                   color='k',        # color de líneas
                   linewidth=lw)     # grosor proporcional a |E|

    #  GRAFICAR LAS CARGAS 
    for _, (xq, yq) in qtopos.items():
        # Dibujamos la carga como un círculo negro
        plt.scatter(xq, yq, color='black', s=100,
                    edgecolors='white', zorder=3)
        # Añadimos el símbolo "+"
        plt.text(xq, yq, '+', color='white',
                 ha='center', va='center',
                 fontsize=12, weight='bold')

    # Configuración de los ejes y apariencia
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.xlim(-boxl, boxl)
    plt.ylim(-boxl, boxl)
    plt.gca().set_aspect('equal')  # escala igual en ambos ejes
    plt.title("Líneas de campo eléctrico (4 cargas positivas)")

    plt.show()


# FUNCIÓN PRINCIPAL: main()
# 
# Ejecuta el programa generando la gráfica del campo eléctrico

def main():
    boxl = 2.0   # semilado de la región a graficar
    n = 40       # número de puntos de malla en cada eje
    plotfield(boxl, n)

if __name__ == "__main__":
    main()