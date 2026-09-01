"""
Gráfica de corriente vs voltaje para luz amarilla a distintos ángulos.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Incertidumbres
DELTA_V = 0.001          # V
DELTA_I = 2e-9           # A
DELTA_I_TABLA = DELTA_I / 1e-8  # en unidades ×10^-8 A

# Datos: corriente (×10^-8 A) y voltaje (V)
datos = {
    r"$\theta = 0$": {
        "I": np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], dtype=float),
        "V": np.array([-0.045, -0.110, -0.130, -0.154, -0.180, -0.182,
                        -0.208, -0.240, -0.270, -0.320, -0.455]),
    },
    r"$\theta = \pi/2$": {
        "I": np.array([5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0], dtype=float),
        "V": np.array([-0.099, -0.101, -0.150, -0.172, -0.180, -0.208,
                        -0.224, -0.265, -0.284, -0.344, -0.403]),
    },
    r"$\theta = 7\pi/4$": {
        "I": np.array([5.5, 5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0], dtype=float),
        "V": np.array([-0.002, -0.012, -0.031, -0.067, -0.097, -0.119,
                        -0.134, -0.157, -0.201, -0.243, -0.384, -0.413]),
    },
    r"$\theta = \pi/4$": {
        "I": np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], dtype=float),
        "V": np.array([-0.001, -0.035, -0.057, -0.081, -0.090, -0.150,
                        -0.190, -0.218, -0.238, -0.300, -0.436]),
    },
}

# Colores y marcadores bien diferenciados para cada ángulo
ESTILOS = {
    r"$\theta = 0$": {"color": "#1f77b4", "marker": "o"},       # azul
    r"$\theta = \pi/2$": {"color": "#d62728", "marker": "s"},   # rojo
    r"$\theta = 7\pi/4$": {"color": "#2ca02c", "marker": "^"},  # verde
    r"$\theta = \pi/4$": {"color": "#9467bd", "marker": "D"},    # morado
}

plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
})

fig, ax = plt.subplots(figsize=(9, 6))

for nombre, serie in datos.items():
    estilo = ESTILOS[nombre]
    ax.errorbar(
        serie["V"],
        serie["I"],
        xerr=DELTA_V,
        yerr=DELTA_I_TABLA,
        fmt=estilo["marker"],
        linestyle="none",
        color=estilo["color"],
        ecolor=estilo["color"],
        elinewidth=1.2,
        capsize=3,
        markersize=5,
        label=nombre,
        alpha=0.9,
    )

ax.set_xlabel(r"Voltaje $V$ (V)")
ax.set_ylabel(r"Corriente $I$ ($\times 10^{-8}\,\mathrm{A}$)")
ax.set_title("Luz amarilla: corriente vs voltaje a distintos ángulos")
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend(title="Ángulo", loc="best")

plt.tight_layout()
plt.savefig("amarillo_angulos_vs_voltaje.png", dpi=300, bbox_inches="tight")
plt.savefig("amarillo_angulos_vs_voltaje.pdf", bbox_inches="tight")
print("Gráficas guardadas: amarillo_angulos_vs_voltaje.png y .pdf")
