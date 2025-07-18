import pandas as pd
import requests
from geopy.geocoders import Nominatim
from time import sleep

# 1. Cargar el archivo Superstore
ventas = pd.read_csv('data/Superstore_top10_ciudades.csv', sep=';', encoding='utf-8')

# 2. Convertir columnas de fecha
ventas['Order Date'] = pd.to_datetime(ventas['Order Date'], dayfirst=True, errors='coerce')

# 3. Filtrar solo columnas necesarias
ventas = ventas[['Order Date', 'City']]
ventas = ventas.rename(columns={'Order Date': 'fecha_venta', 'City': 'ciudad'})

# 4. Obtener ciudades únicas
ciudades = ventas['ciudad'].dropna().unique()

# 5. Usar geopy para obtener lat/lon de cada ciudad
print("📍 Obteniendo coordenadas...")
geolocator = Nominatim(user_agent="superstore_clima")
coordenadas = {}

for ciudad in ciudades:
    try:
        location = geolocator.geocode(f"{ciudad}, Colombia", timeout=10)
        if location:
            coordenadas[ciudad] = (location.latitude, location.longitude)
            print(f"✅ {ciudad}: {location.latitude}, {location.longitude}")
        else:
            print(f"⚠️ No se encontró ubicación para: {ciudad}")
    except Exception as e:
        print(f"❌ Error geolocalizando {ciudad}: {e}")
    sleep(1.2)  # evitar bloqueo de API de geolocalización

# 6. Obtener fechas únicas
fechas = ventas['fecha_venta'].dropna().dt.date.unique()
fecha_min = str(min(fechas))
fecha_max = str(max(fechas))

# 7. Obtener clima por ciudad
print("\n🌤️ Consultando clima por ciudad...")
datos_clima = []

for ciudad, (lat, lon) in coordenadas.items():
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={fecha_min}&end_date={fecha_max}"
        f"&daily=temperature_2m_max,temperature_2m_min,rain_sum"
        f"&timezone=America/Bogota"
    )
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            clima_json = respuesta.json()
            for i, fecha in enumerate(clima_json['daily']['time']):
                datos_clima.append({
                    'fecha_venta': fecha,
                    'ciudad': ciudad,
                    'temperatura_maxima': clima_json['daily']['temperature_2m_max'][i],
                    'temperatura_minima': clima_json['daily']['temperature_2m_min'][i],
                    'lluvia_mm': clima_json['daily']['rain_sum'][i]
                })
            print(f"✅ Clima cargado para {ciudad}")
        else:
            print(f"❌ Fallo al obtener clima para {ciudad} - Código {respuesta.status_code}")
    except Exception as e:
        print(f"❌ Error en {ciudad}: {e}")
    sleep(1.2)

# 8. Convertir datos de clima a DataFrame
clima_df = pd.DataFrame(datos_clima)
clima_df['fecha_venta'] = pd.to_datetime(clima_df['fecha_venta'])

# 9. Unir clima con ventas
ventas = pd.read_csv('data/Superstore.csv', sep=';', encoding='utf-8')
ventas['Order Date'] = pd.to_datetime(ventas['Order Date'], dayfirst=True, errors='coerce')
ventas = ventas.rename(columns={'Order Date': 'fecha_venta', 'City': 'ciudad'})

ventas_clima = pd.merge(ventas, clima_df, on=['fecha_venta', 'ciudad'], how='left')

# 10. Guardar archivo final
ventas_clima.to_csv('data/Superstore_con_clima.csv', index=False, encoding='utf-8')
print("\n💾 Archivo guardado: data/Superstore_con_clima.csv")
