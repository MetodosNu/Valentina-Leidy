"""
Implementar una clase que realice derivación automática usando métodos mágicos y atributos para definir 
los números duales y sus operaciones.
"""

import math   # Importamos la librería math para usar funciones como sin, cos, exp, log

# Clase Dual: define un número dual

class Dual:
    def __init__(self, real, dual=0.0):
        """
        Constructor de la clase Dual.
        real -> parte real del número (el valor de la función).
        dual -> parte dual (transporta la derivada).
        """
        self.real = real
        self.dual = dual

    def __repr__(self):
        """
        Representación en texto de un número dual.
        Ejemplo: 2 + 3ε
        """
        return f"{self.real} + {self.dual}ε"

    # Operaciones básicas con números duales 

    def __add__(self, other):
        """Suma de números duales"""
        other = self._to_dual(other)  # Aseguramos que 'other' sea Dual
        return Dual(self.real + other.real, self.dual + other.dual)

    def __sub__(self, other):
        """Resta de números duales"""
        other = self._to_dual(other)
        return Dual(self.real - other.real, self.dual - other.dual)

    def __mul__(self, other):
        """Multiplicación de números duales"""
        other = self._to_dual(other)
        # (a + bε)(c + dε) = ac + (ad + bc)ε
        return Dual(self.real * other.real,
                    self.real * other.dual + self.dual * other.real)

    def __truediv__(self, other):
        """División de números duales"""
        other = self._to_dual(other)
        # (a + bε) / (c + dε) = (a/c) + ((bc - ad)/c^2) ε
        return Dual(self.real / other.real,
                    (self.dual * other.real - self.real * other.dual) / (other.real**2))

    def __pow__(self, n):
        """Potencia de un número dual con exponente entero"""
        # (x + ε dx)^n = x^n + n x^(n-1) dx ε
        return Dual(self.real**n, n * (self.real**(n-1)) * self.dual)

    # Método auxiliar 
    def _to_dual(self, other):
        """
        Convierte números reales a duales.
        Ejemplo: 3 -> Dual(3, 0)
        """
        if isinstance(other, Dual):
            return other
        return Dual(other, 0.0)

# Funciones matemáticas extendidas

def sin(x):
    """Seno de un número dual"""
    return Dual(math.sin(x.real), math.cos(x.real) * x.dual)

def cos(x):
    """Coseno de un número dual"""
    return Dual(math.cos(x.real), -math.sin(x.real) * x.dual)

def exp(x):
    """Exponencial de un número dual"""
    return Dual(math.exp(x.real), math.exp(x.real) * x.dual)

def log(x):
    """Logaritmo natural de un número dual"""
    return Dual(math.log(x.real), (1 / x.real) * x.dual)

# Programa principal 

if __name__ == "__main__":
    print("=== Derivación automática con números duales ===")

    # Pedir valor donde se quiere evaluar
    a = float(input("Ingresa el punto donde quieres evaluar la función (ej: 2): "))

    # Crear número dual (dual=1 para obtener derivada)
    x = Dual(a, 1.0)

    # Pedir función al usuario
    print("\nEscribe la función en términos de x.")
    print("Ejemplos:")
    print(" - x**3")
    print(" - sin(x) + x**2")
    print(" - exp(x) / x")
    print(" - log(x) + cos(x)")

    funcion_str = input("f(x) = ")

    # Evaluar la función usando eval
    f = eval(funcion_str)

    # Mostrar resultados
    print("\n--- Resultado ---")
    print(f"Función evaluada en x={a}: {f.real}")
    print(f"Derivada en x={a}: {f.dual}")
    print(f"Número dual completo: {f}")

