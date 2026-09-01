"""
Gráfica de intensidad (corriente) vs voltaje para el efecto fotoeléctrico.
Cuatro colores de luz: azul, rojo, verde y amarillo.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Corriente: valores de la tabla (todos en unidades de 10^-8 A)
I_TABLA = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], dtype=float)
I = I_TABLA * 1e-8  # corriente en amperios (A)

# Voltajes en V
datos = {
    "Azul": np.array([-0.136, -0.236, -0.273, -0.310, -0.352, -0.385,
                      -0.435, -0.458, -0.527, -0.624, -0.870]),
    "Rojo": np.array([-0.091, -0.125, -0.142, -0.150, -0.168, -0.180,
                      -0.197, -0.214, -0.234, -0.257, -0.367]),
    "Verde": np.array([-0.121, -0.205, -0.242, -0.260, -0.286, -0.321,
                       -0.375, -0.408, -0.447, -0.520, -0.760]),
    "Amarillo": np.array([-0.045, -0.110, -0.130, -0.154, -0.180, -0.182,
                          -0.208, -0.240, -0.270, -0.320, -0.455]),
}

# Incertidumbres
DELTA_V = 0.001          # V
DELTA_I = 2e-9           # A

COLORES = {
    "Azul": "#1f77b4",
    "Rojo": "#d62728",
    "Verde": "#2ca02c",
    "Amarillo": "#ffbf00",
}

plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
})

fig, ax = plt.subplots(figsize=(9, 6))

for nombre, voltaje in datos.items():
    ax.errorbar(
        voltaje,
        I_TABLA,
        xerr=DELTA_V,
        yerr=DELTA_I / 1e-8,  # incertidumbre en unidades de la tabla (×10^-8 A)        fmt="o",
        color=COLORES[nombre],
        ecolor=COLORES[nombre],
        elinewidth=1.2,
        capsize=3,
        markersize=5,
        label=nombre,
        alpha=0.9,
    )

ax.set_xlabel(r"Voltaje $V$ (V)")
ax.set_ylabel(r"Corriente $I$ ($\times 10^{-8}\,\mathrm{A}$)")
ax.set_title("Efecto fotoeléctrico: intensidad vs voltaje")
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend(title="Color de luz", loc="best")

plt.tight_layout()
plt.savefig("intensidad_vs_voltaje.png", dpi=300, bbox_inches="tight")
plt.savefig("intensidad_vs_voltaje.pdf", bbox_inches="tight")
print("Gráficas guardadas: intensidad_vs_voltaje.png y .pdf")
