"""
K_max vs f con recta de regresión y panel de residuales.
Usa las ecuaciones de la pizarra (FWHM, σ_f, σ_K, K = mf + b).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

C = 299792458.0
E_CHARGE = 1.602176634e-19

DELTA_V = 0.001
FWHM_NM = 30.0
SIGMA_LAMBDA_NM = FWHM_NM / 2.35

LAMBDA_NM = {
    "Azul": 469.0,
    "Verde": 567.0,
    "Amarillo": 590.0,
    "Rojo": 659.0,
}
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
    datos = []
    for nombre in ORDEN:
        lam_nm = LAMBDA_NM[nombre]
        lam_m = lam_nm * 1e-9
        sigma_lam_m = SIGMA_LAMBDA_NM * 1e-9

        f = C / lam_m
        sigma_f = (f / lam_m) * sigma_lam_m  # σ_f = (f/λ) σ_λ

        k_ev = V_STOP[nombre]
        k_j = E_CHARGE * k_ev
        sigma_k_ev = DELTA_V
        sigma_k_j = E_CHARGE * DELTA_V

        datos.append({
            "nombre": nombre,
            "lambda_nm": lam_nm,
            "f": f,
            "sigma_f": sigma_f,
            "k_ev": k_ev,
            "sigma_k_ev": sigma_k_ev,
            "k_j": k_j,
            "sigma_k_j": sigma_k_j,
        })
    return datos


def regresion_ponderada(f, k, sigma_k):
    """K = m f + b con pesos w = 1/σ_K²."""
    w = 1.0 / sigma_k**2
    W = np.diag(w)
    X = np.column_stack([f, np.ones(len(f))])
    cov = np.linalg.inv(X.T @ W @ X)
    m, b = cov @ X.T @ W @ k
    sigma_m = np.sqrt(cov[0, 0])
    sigma_b = np.sqrt(cov[1, 1])

    k_pred = m * f + b
    residuales = k - k_pred
    # σ_r efectiva: contribución de σ_K y de σ_f a través de la pendiente
    return m, b, sigma_m, sigma_b, k_pred, residuales


def graficar_con_residuales(datos, unidad, archivo_base):
    nombres = [d["nombre"] for d in datos]
    f = np.array([d["f"] for d in datos])
    sigma_f = np.array([d["sigma_f"] for d in datos])

    if unidad == "eV":
        k = np.array([d["k_ev"] for d in datos])
        sigma_k = np.array([d["sigma_k_ev"] for d in datos])
        ylab = r"$K_{\max}$ (eV)"
        ylab_res = r"Residuo $r$ (eV)"
        factor = 1.0
    else:
        k = np.array([d["k_j"] for d in datos])
        sigma_k = np.array([d["sigma_k_j"] for d in datos])
        ylab = r"$K_{\max}$ (J)"
        ylab_res = r"Residuo $r$ (J)"
        factor = E_CHARGE

    m, b, sigma_m, sigma_b, k_pred, residuales = regresion_ponderada(f, k, sigma_k)

    # Incertidumbre del residual: σ_r = sqrt(σ_K² + (m σ_f)²)
    sigma_r = np.sqrt(sigma_k**2 + (m * sigma_f)**2)
    residuales_norm = residuales / sigma_r

    f0 = -b / m
    sigma_f0 = np.sqrt((sigma_b / m)**2 + (b * sigma_m / m**2)**2)
    phi = -b
    h = m

    print(f"\n=== {unidad} ===")
    print(f"m = h = {h:.6e} ± {sigma_m:.6e}")
    print(f"b = {b:.6e} ± {sigma_b:.6e}")
    print(f"φ = {phi:.6e} ± {sigma_b:.6e}")
    print(f"f0 = {f0:.6e} ± {sigma_f0:.6e} Hz")
    for i, nombre in enumerate(nombres):
        print(f"  {nombre}: K={k[i]:.6e}, ŷ={k_pred[i]:.6e}, "
              f"r={residuales[i]:+.6e}, σ_r={sigma_r[i]:.6e}, "
              f"r/σ_r={residuales_norm[i]:+.3f}")

    # ---- figura: ajuste + residuales ----
    fig, (ax, axr) = plt.subplots(
        2, 1, figsize=(9, 8), sharex=True,
        gridspec_kw={"height_ratios": [2.4, 1], "hspace": 0.05},
    )

    # Recta de regresión
    f_line = np.linspace(min(f) - 0.15 * (max(f) - min(f)),
                         max(f) + 0.05 * (max(f) - min(f)), 200)
    # restringir a K >= 0 para visualización física en el trazo principal
    k_line = m * f_line + b
    ax.plot(
        f_line, k_line, color="black", linewidth=1.8, zorder=1,
        label=rf"$K = mf + b$" + "\n"
              + rf"$h=({h/factor:.3e}\pm{sigma_m/factor:.1e})$ "
              + (r"eV$\cdot$s" if unidad == "eV" else r"J$\cdot$s") + "\n"
              + rf"$f_0=({f0/1e14:.3f}\pm{sigma_f0/1e14:.3f})\times 10^{{14}}$ Hz",
    )

    # Marcar f0 (corte con K=0)
    if f0 > 0:
        ax.axvline(f0, color="gray", linestyle=":", linewidth=1.2, alpha=0.8)
        ax.axhline(0, color="gray", linestyle=":", linewidth=1.0, alpha=0.6)
        ax.scatter([f0], [0], color="black", marker="x", s=60, zorder=5,
                   label=r"$f_0$ ($K=0$)")

    for i, nombre in enumerate(nombres):
        ax.errorbar(
            f[i], k[i],
            xerr=sigma_f[i], yerr=sigma_k[i],
            fmt="o", linestyle="none",
            color=COLORES[nombre], ecolor=COLORES[nombre],
            elinewidth=1.2, capsize=3, markersize=7,
            label=nombre, zorder=3,
        )

    ax.set_ylabel(ylab)
    ax.set_title(r"$K_{\max}$ vs $f$ con regresión lineal y residuales")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="best", fontsize=8)
    ax.ticklabel_format(axis="x", style="scientific", scilimits=(0, 0))
    if unidad == "J":
        ax.ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))

    # Panel de residuales
    axr.axhline(0, color="black", linewidth=1.2)
    for i, nombre in enumerate(nombres):
        axr.errorbar(
            f[i], residuales[i],
            xerr=sigma_f[i], yerr=sigma_r[i],
            fmt="o", linestyle="none",
            color=COLORES[nombre], ecolor=COLORES[nombre],
            elinewidth=1.2, capsize=3, markersize=6,
        )
    axr.set_xlabel(r"Frecuencia $f$ (Hz)")
    axr.set_ylabel(ylab_res)
    axr.grid(True, linestyle="--", alpha=0.4)
    axr.ticklabel_format(axis="x", style="scientific", scilimits=(0, 0))
    if unidad == "J":
        axr.ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))

    plt.savefig(f"{archivo_base}.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{archivo_base}.pdf", bbox_inches="tight")
    print(f"Guardado: {archivo_base}.png y .pdf")
    plt.close(fig)


def main():
    datos = calcular_datos()
    graficar_con_residuales(datos, "eV", "energia_cinetica_eV_vs_frecuencia")
    graficar_con_residuales(datos, "J", "energia_cinetica_J_vs_frecuencia")


if __name__ == "__main__":
    main()
