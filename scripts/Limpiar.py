import pandas as pd

# Ruta al archivo original
ruta_entrada = "data/ventas_predichas_solo_clima.csv"

# Ruta para guardar el archivo limpio
ruta_salida = "data/ventas_predichas_limpio.csv"

# Cargar el archivo original
df = pd.read_csv(ruta_entrada)

# Asegurar conversión correcta de columnas numéricas
df['Sales'] = df['Sales'].astype(str).str.replace(',', '.').str.replace('$', '', regex=False)
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

# Calcular precio_unitario
df['precio_unitario'] = df['Sales'] / df['Quantity']

# Renombrar columnas según lo que espera Supabase
df['total_venta'] = df['Sales']
df['ventas_predichas'] = df['ventas_predichas_clima']

# Filtrar columnas finales para Supabase
columnas_finales = [
    "fecha_venta",
    "ciudad",
    "temperatura_maxima",
    "temperatura_minima",
    "lluvia_mm",
    "precio_unitario",
    "total_venta",
    "ventas_predichas"
]

df_filtrado = df[columnas_finales]

# Guardar el archivo limpio
df_filtrado.to_csv(ruta_salida, index=False)

print(f"✅ Archivo limpio guardado como: {ruta_salida}")
