"""
Energía cinética máxima vs frecuencia para los cuatro colores del efecto fotoeléctrico.

La frecuencia se obtiene de longitudes de onda teóricas (líneas espectrales del Hg).
La energía cinética se obtiene del potencial de frenado medido (I = 0 en las tablas).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Constantes
C = 299792458.0                    # m/s
E_CHARGE = 1.602176634e-19         # C
EV_TO_J = E_CHARGE                 # 1 eV en joules

# Incertidumbres experimentales
DELTA_V = 0.001                    # V (voltímetro)
DELTA_LAMBDA_NM = 0.1              # nm (incertidumbre en λ teórica de la línea)

# Longitudes de onda teóricas (nm) — líneas del vapor de mercurio usadas en laboratorio
# Azul: 435.8 nm | Verde: 546.1 nm | Amarillo: 577.0–579.1 nm (promedio 578.0)
# Rojo: filtro rojo típico ~700 nm (Hg no tiene línea roja intensa)
LAMBDA_NM = {
    "Azul": 435.8,
    "Verde": 546.1,
    "Amarillo": 578.0,
    "Rojo": 700.0,
}

# Potencial de frenado |V_s| en V (dato experimental, I = 0)
V_STOP = {
    "Azul": 0.870,
    "Verde": 0.760,
    "Amarillo": 0.455,
    "Rojo": 0.367,
}

COLORES = {
    "Azul": "#1f77b4",
    "Verde": "#2ca02c",
    "Amarillo": "#ffbf00",
    "Rojo": "#d62728",
}

ORDEN = ["Azul", "Verde", "Amarillo", "Rojo"]


def calcular_datos():
    """Calcula f, K (J y eV) y sus incertidumbres."""
    resultados = []
    for nombre in ORDEN:
        lam_nm = LAMBDA_NM[nombre]
        lam_m = lam_nm * 1e-9
        delta_lam_m = DELTA_LAMBDA_NM * 1e-9

        # f = c / λ
        f = C / lam_m
        delta_f = (C / lam_m**2) * delta_lam_m

        # K_max = e * V_s  (J)  ;  K_max (eV) = V_s
        v_s = V_STOP[nombre]
        k_j = E_CHARGE * v_s
        k_ev = v_s
        delta_k_j = E_CHARGE * DELTA_V
        delta_k_ev = DELTA_V

        resultados.append({
            "nombre": nombre,
            "lambda_nm": lam_nm,
            "f_hz": f,
            "delta_f_hz": delta_f,
            "k_j": k_j,
            "delta_k_j": delta_k_j,
            "k_ev": k_ev,
            "delta_k_ev": delta_k_ev,
        })
    return resultados


def imprimir_calculos(datos):
  """Imprime resumen numérico para el informe."""
  print("\n=== Cálculos ===")
  print(f"{'Color':<10} {'λ (nm)':>8} {'f (Hz)':>14} {'Δf (Hz)':>12} "
        f"{'K (eV)':>8} {'K (J)':>12} {'ΔK (J)':>12}")
  for d in datos:
      print(f"{d['nombre']:<10} {d['lambda_nm']:8.1f} {d['f_hz']:14.3e} "
            f"{d['delta_f_hz']:12.3e} {d['k_ev']:8.3f} {d['k_j']:12.3e} "
            f"{d['delta_k_j']:12.3e}")


def graficar(datos, unidad, archivo_base):
    """Genera gráfica K vs f en eV o J."""
    fig, ax = plt.subplots(figsize=(9, 6))

    for d in datos:
        nombre = d["nombre"]
        if unidad == "eV":
            y, dy = d["k_ev"], d["delta_k_ev"]
            ylab = r"Energía cinética máxima $K_{\max}$ (eV)"
        else:
            y, dy = d["k_j"], d["delta_k_j"]
            ylab = r"Energía cinética máxima $K_{\max}$ (J)"

        ax.errorbar(
            d["f_hz"],
            y,
            xerr=d["delta_f_hz"],
            yerr=dy,
            fmt="o",
            linestyle="none",
            color=COLORES[nombre],
            ecolor=COLORES[nombre],
            elinewidth=1.2,
            capsize=3,
            markersize=7,
            label=nombre,
        )

    ax.set_xlabel(r"Frecuencia $f$ (Hz)")
    ax.set_ylabel(ylab)
    ax.set_title(r"$K_{\max}$ vs $f$ — efecto fotoeléctrico")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(title="Color", loc="best")
    ax.ticklabel_format(axis="x", style="scientific", scilimits=(0, 0))
    if unidad == "J":
        ax.ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))

    plt.tight_layout()
    plt.savefig(f"{archivo_base}.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{archivo_base}.pdf", bbox_inches="tight")
    print(f"Guardado: {archivo_base}.png y .pdf")


def main():
    datos = calcular_datos()
    imprimir_calculos(datos)
    graficar(datos, "eV", "energia_cinetica_eV_vs_frecuencia")
    graficar(datos, "J", "energia_cinetica_J_vs_frecuencia")


if __name__ == "__main__":
    main()
