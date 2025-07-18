import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar el archivo CSV usando punto y coma como separador
ruta_archivo = 'data/Superstore.csv'

try:
    df = pd.read_csv(ruta_archivo, sep=';', encoding='utf-8')
    print("✅ Archivo cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el archivo: {e}")
    exit()

# 2. Mostrar las primeras filas
print("\n🔍 Primeras filas del archivo:")
print(df.head())

# 3. Convertir columnas de fecha (formato día/mes/año)
for col in ['Order Date', 'Ship Date']:
    try:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
        print(f"✅ {col} convertido correctamente.")
    except:
        print(f"❌ Error al convertir {col}.")

# 4. Convertir columnas numéricas que tienen coma como separador decimal
for col in ['Sales', 'Discount', 'Profit']:
    try:
        df[col] = df[col].str.replace(',', '.', regex=False).astype(float)
        print(f"✅ {col} convertido a numérico.")
    except:
        print(f"❌ Error al convertir {col}.")

# 5. Revisar tipos de datos
print("\n🔧 Tipos de datos:")
print(df.dtypes)

# 6. Verificar valores faltantes
print("\n🧼 Valores faltantes por columna:")
print(df.isnull().sum())

# 7. Resumen estadístico de variables numéricas
print("\n📊 Estadísticas descriptivas:")
print(df[['Sales', 'Quantity', 'Discount', 'Profit']].describe())

# 8. Gráfico: ventas totales por categoría
print("\n📈 Generando gráfico de ventas por categoría...")
df.groupby('Category')['Sales'].sum().plot(
    kind='bar',
    title='Ventas totales por categoría',
    figsize=(8, 5),
    color='skyblue'
)
plt.ylabel('Ventas (USD)')
plt.xlabel('Categoría')
plt.tight_layout()
plt.show()
