import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar archivo de ventas con clima
df = pd.read_csv('data/Superstore_con_clima.csv', sep=',', encoding='utf-8')

# 2. Convertir columnas numéricas que estén en formato texto (coma como separador decimal)
for col in ['Sales', 'Profit', 'Discount']:
    df[col] = df[col].astype(str).str.replace(',', '.').str.replace('$', '', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 3. Crear 'precio_unitario_pesos' si no existe
if 'precio_unitario_pesos' not in df.columns:
    df['precio_unitario_pesos'] = df['Sales'] / df['Quantity']

# 4. Filtrar columnas relevantes para análisis de correlación
columnas_correlacion = [
    'temperatura_maxima', 'temperatura_minima', 'lluvia_mm',
    'Sales', 'Profit', 'Discount', 'Quantity', 'precio_unitario_pesos'
]
columnas_disponibles = [col for col in columnas_correlacion if col in df.columns]
df_cor = df[columnas_disponibles].dropna()

# 5. Calcular matriz de correlación
correlacion = df_cor.corr()

# 6. Visualizar con mapa de calor usando seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(correlacion, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Mapa de calor de correlación: clima vs ventas')
plt.tight_layout()
plt.show()
