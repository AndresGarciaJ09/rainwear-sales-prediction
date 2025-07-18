import pandas as pd

# 1. Cargar archivo original
df = pd.read_csv('data/Superstore.csv', sep=';', encoding='utf-8')

# 2. Obtener las 10 ciudades con más registros
top_ciudades = df['City'].value_counts().head(10).index.tolist()

# 3. Filtrar solo esas ciudades
df_filtrado = df[df['City'].isin(top_ciudades)]

# 4. Guardar el nuevo archivo
df_filtrado.to_csv('data/Superstore_top10_ciudades.csv', index=False, sep=';', encoding='utf-8')

# 5. Confirmar en consola
print("✅ Archivo filtrado guardado como: data/Superstore_top10_ciudades.csv")
print(f"Ciudades incluidas: {top_ciudades}")
