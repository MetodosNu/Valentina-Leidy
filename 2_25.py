# multipole_225.py
# Generalización del ejercicio 2.25:
# Funciona tanto si el punto de observación está fuera (r > max|ri|) como dentro (r < min|ri|).

"""
Generaliza el código multipole.py para que funcione independientemente de si r > ri o no. Esto requiere hacer 
cambios en las tres funciones de ese programa.
"""

from kahansum import kahansum
from chargearray import chargearray, vecmag, fullpot
from legendre import legendre

EPS = 1e-12  # EPS: epsilon numérico. Valor muy pequeño para evitar divisiones por cero

def decomp(rs, ri):
    """
    Descomposición geométrica entre el punto de observación 'rs' y la posición de una carga 'ri'.

    Parámetros:
      rs : coordenadas del punto de observación, p.ej. [x, y]
      ri : coordenadas de la i-ésima carga, p.ej. [xi, yi]

    Retorna:
      rmag    = |rs|
      rimag   = |ri|
      costheta = cos(θ) siendo θ el ángulo entre rs y ri

    Notas:
      - Si rmag*rimag == 0, definimos costheta = 0 para evitar 0/0.
      - Luego "recortamos" costheta a [-1, 1] para protegernos de errores numéricos
        y que P_n(x) (Legendre) reciba un argumento válido.
    """
    rmag = vecmag(rs) # |rs|   (magnitud del vector "rs")
    rimag = vecmag(ri) # |ri|   (magnitud del vector "ri")
    # Producto punto rs·ri:
    prs = [r * ri_ for r, ri_ in zip(rs, ri)]  # producto punto
    vecdot = kahansum(prs)
    costheta = (vecdot / (rmag * rimag)) if (rmag * rimag) != 0 else 0.0
    # Por redondeos de punto flotante podría salir algo como 1.0000000002 o -1.0000000003.
    # Legendre P_n(x) está definido para |x|<=1. Por eso "clampeamos" (recortamos) el valor.
    if costheta > 1.0: costheta = 1.0
    if costheta < -1.0: costheta = -1.0
    return rmag, rimag, costheta

def multicoes(rs, qtopos, nmax, regime):
    """
    Construye los coeficientes de la expansión multipolar HASTA orden nmax.
    - regime = 'outside'  → V(r) = sum_n [ coes[n] / r^(n+1) ]
      con coes[n] = sum_i q_i * r_i^n * P_n(cosθ_i)
    - regime = 'inside'   → V(r) = sum_n [ coes[n] * r^n ]
      con coes[n] = sum_i q_i * P_n(cosθ_i) / r_i^(n+1)

    Esto es exactamente la generalización que pide el 2.25.
    """
    coes = [0.0 for _ in range(nmax + 1)]
    
    for q, pos in qtopos.items():
        rmag, rimag, costheta = decomp(rs, pos)
        # Para cada orden n, sumamos la contribución de esta carga a coes[n]
        for n in range(nmax + 1):
            Pn = legendre(n, costheta)[0] # legendre(n, x) -> (P_n(x), P'_n(x))
            if regime == 'outside':
                # Observador lejos: expansión en potencias de (ri^n) / r^(n+1)
                val = q * (rimag ** n) * Pn
            else:  # 'inside'
                # Observador cerca del origen: expansión en potencias de r^n / (ri^(n+1))
                denom = (rimag ** (n + 1)) if rimag > EPS else float('inf')
                val = q * Pn / denom
            coes[n] += val
    return coes

def multifullpot(rs, qtopos, nmax=60):
    """
    Ensambla el potencial en 'rs' usando la expansión multipolar adecuada.

    Decisión del RÉGIMEN ('regime'):
      - 'outside' si |rs| > Rmax  (con margen EPS)
      - 'inside'  si |rs| < Rmin  (con margen EPS)
      - si |rs| está en la "zona intermedia" (entre Rmin y Rmax), ninguna de las
        dos series está garantizada a converger estrictamente. En ese caso elegimos 
        la más razonable (outside si |rs| > promedio, si no inside).
    """
    rmag = vecmag(rs)
    # Rmin y Rmax: los radios mínimo y máximo de las posiciones de las cargas.
    magnitudes = [vecmag(pos) for pos in qtopos.values()]
    Rmax = max(magnitudes)
    Rmin = min(magnitudes)

    # Elegimos el régimen según dónde cae |rs| respecto al anillo [Rmin, Rmax].
    
    if rmag > Rmax + EPS:
        regime = 'outside'
    elif rmag < Rmin - EPS:
        regime = 'inside'
    else:
        # Zona intermedia: la teoría estricta no garantiza convergencia uniforme.
        # Elegimos una heurística simple para tener un resultado numérico útil.
        mid = 0.5 * (Rmin + Rmax)
        regime = 'outside' if rmag >= mid else 'inside'

    coes = multicoes(rs, qtopos, nmax, regime)

    # Ensamble final según el régimen
    contribs = []
    if regime == 'outside':
        # V(r) = sum_n coes[n] / r^(n+1)
        if rmag < EPS:
            return 0.0, regime  # evitamos 1/0 si rs=0
        for n, coe in enumerate(coes):
            contribs.append(coe / (rmag ** (n + 1)))
    else:
        # 'inside': V(r) = sum_n coes[n] * r^n
        for n, coe in enumerate(coes):
            contribs.append(coe * (rmag ** n))

    return kahansum(contribs), regime

if __name__ == '__main__':
    # Conjunto de cargas de prueba
    qtopos = chargearray(6)

    # Punto “afuera” (típico en el original): |rs| > max|ri|
    rs_out = [2.0, 0.0]
    V_out, reg_out = multifullpot(rs_out, qtopos, nmax=60)
    V_out_exact = fullpot(qtopos, rs_out)

    # Punto “adentro”: |rs| < min|ri|
    rs_in = [0.01, 0.0]
    V_in, reg_in = multifullpot(rs_in, qtopos, nmax=60)
    V_in_exact = fullpot(qtopos, rs_in)

    print(f"rs_out = {rs_out}  régimen = {reg_out:>7}  V_multipolar = {V_out:.8f}  V_exacto = {V_out_exact:.8f}")
    print(f"rs_in  = {rs_in}   régimen = {reg_in:>7}  V_multipolar = {V_in:.8f}  V_exacto = {V_in_exact:.8f}")
