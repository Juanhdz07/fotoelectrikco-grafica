# Gráfica efecto fotoeléctrico — Intensidad vs voltaje

Script en Python para graficar corriente (intensidad) frente a voltaje con barras de error, para cuatro colores de luz (azul, rojo, verde, amarillo).

## Datos

Los valores de corriente en la tabla se expresan como $I \times 10^{-8}\,\mathrm{A}$ (por ejemplo, 10 → $10 \times 10^{-8}\,\mathrm{A}$).

## Incertidumbres

- Voltaje: \(\Delta V = 0{,}001\,\mathrm{V}\)
- Corriente: \(\Delta I = 2 \times 10^{-9}\,\mathrm{A} = 0{,}2 \times 10^{-8}\,\mathrm{A}\) (en unidades de la tabla)

## Uso

```bash
pip install -r requirements.txt
python grafica_fotoelectrico.py
```

Genera `intensidad_vs_voltaje.png` y `intensidad_vs_voltaje.pdf`.

### Luz amarilla a distintos ángulos

```bash
python grafica_amarillo_angulos.py
```

Genera `amarillo_angulos_vs_voltaje.png` y `amarillo_angulos_vs_voltaje.pdf` para los ángulos
$\theta = 0$, $\pi/2$, $7\pi/4$ y $\pi/4$.

### Energía cinética vs frecuencia (cuatro colores)

```bash
python grafica_energia_cinetica_vs_frecuencia.py
```

Genera `energia_cinetica_eV_vs_frecuencia.png/.pdf` y `energia_cinetica_J_vs_frecuencia.png/.pdf`.
La frecuencia se calcula con $f = c/\lambda$ a partir de los picos LED
(azul 469 nm, verde 567 nm, ámbar 590 nm, rojo 659 nm; FWHM $\approx 30$ nm).
$K_{\max}$ se obtiene del potencial de frenado experimental ($I = 0$).
