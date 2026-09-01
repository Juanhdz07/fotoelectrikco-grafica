# Gráfica efecto fotoeléctrico — Intensidad vs voltaje

Script en Python para graficar corriente (intensidad) frente a voltaje con barras de error, para cuatro colores de luz (azul, rojo, verde, amarillo).

## Incertidumbres

- Voltaje: \(\Delta V = 0{,}001\,\mathrm{V}\)
- Corriente: \(\Delta I = 2 \times 10^{-9}\,\mathrm{A}\)

## Uso

```bash
pip install -r requirements.txt
python grafica_fotoelectrico.py
```

Genera `intensidad_vs_voltaje.png` y `intensidad_vs_voltaje.pdf`.
