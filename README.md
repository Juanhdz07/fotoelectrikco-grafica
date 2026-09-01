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
