import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# 1. Cargar el dataset
df = pd.read_csv('data/Superstore_con_clima.csv', sep=',', encoding='utf-8')

# 2. Convertir fecha
df['fecha_venta'] = pd.to_datetime(df['fecha_venta'], errors='coerce')

# 3. Limpiar columnas con formato numérico incorrecto
columnas_a_convertir = ['Sales']
for col in columnas_a_convertir:
    df[col] = df[col].astype(str).str.replace(',', '.').str.replace('$', '', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 4. Eliminar filas con valores nulos relevantes
df = df.dropna(subset=['Sales', 'temperatura_maxima', 'temperatura_minima', 'lluvia_mm'])

# 5. Definir X (entradas) y y (salida)
X = df[['temperatura_maxima', 'temperatura_minima', 'lluvia_mm']]
y = df['Sales']  # En USD

# 6. Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Entrenar modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# 8. Evaluación
predicciones = modelo.predict(X_test)
mae = mean_absolute_error(y_test, predicciones)
r2 = r2_score(y_test, predicciones)

print(f"📊 MAE: {mae:,.2f} USD")
print(f"📈 R²: {r2:.2f}")

# 9. Guardar resultados
df['ventas_predichas_clima'] = modelo.predict(X)
df.to_csv('data/ventas_predichas_solo_clima.csv', index=False, encoding='utf-8')
print("💾 Archivo guardado: data/ventas_predichas_solo_clima.csv")

# 10. Visualización opcional
plt.figure(figsize=(8, 6))
plt.scatter(y_test, predicciones, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Línea ideal')
plt.xlabel('Ventas reales (USD)')
plt.ylabel('Ventas predichas (USD)')
plt.title('Relación entre ventas reales y predichas (solo clima)')
plt.legend()
plt.tight_layout()
plt.show()
