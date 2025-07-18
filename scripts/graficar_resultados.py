import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar archivo con predicciones
df = pd.read_csv('data/ventas_predichas_solo_clima.csv')
df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])

# 2. Calcular error absoluto (ventas reales = Sales, predichas = ventas_predichas_clima)
df['error_absoluto'] = abs(df['Sales'] - df['ventas_predichas_clima'])

# ----------------------------------------
# 1. Gráfico de líneas: reales vs. predichas
# ----------------------------------------
df = df.sort_values('fecha_venta')
plt.figure(figsize=(14, 5))
plt.plot(df['fecha_venta'], df['Sales'], label='Ventas reales', linewidth=1.5)
plt.plot(df['fecha_venta'], df['ventas_predichas_clima'], label='Ventas predichas', linestyle='--', linewidth=1.5)
plt.title('Ventas reales vs. Ventas predichas por fecha (solo clima)')
plt.xlabel('Fecha')
plt.ylabel('Total venta (USD)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# 2. Dispersión: ventas reales vs. predichas
# -----------------------------------------------------
plt.figure(figsize=(6, 6))
plt.scatter(df['Sales'], df['ventas_predichas_clima'], alpha=0.6)
plt.plot([df['Sales'].min(), df['Sales'].max()],
         [df['Sales'].min(), df['Sales'].max()],
         color='red', linestyle='--', linewidth=1.5, label='Línea ideal')
plt.xlabel('Ventas reales (USD)')
plt.ylabel('Ventas predichas (USD)')
plt.title('Relación entre ventas reales y predichas (solo clima)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------------------------------------
# 3. Histograma del error absoluto
# ----------------------------------------
plt.figure(figsize=(8, 4))
plt.hist(df['error_absoluto'], bins=30, color='purple', edgecolor='black')
plt.title('Distribución del error absoluto (solo clima)')
plt.xlabel('Error absoluto (USD)')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.show()
