from supabase import create_client, Client
import pandas as pd

# Credenciales de Supabase
url = "https://zblxsowtlzdearbcjytw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpibHhzb3d0bHpkZWFyYmNqeXR3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Mjg0NjcxMSwiZXhwIjoyMDY4NDIyNzExfQ.vmfwrEUgXSezPn4G7CgfUv6jj8ZPDsqp4tKo_UkkrT8"
supabase: Client = create_client(url, key)

# Cargar DataFrame
df = pd.read_csv("data/ventas_predichas_limpio.csv")

# Convertir a lista de diccionarios
data_list = df.to_dict(orient="records")

# Insertar en bloques si hay muchos registros (ej. en lotes de 500)
batch_size = 500
for i in range(0, len(data_list), batch_size):
    batch = data_list[i:i+batch_size]
    supabase.table("ventas_predichas_clima").insert(batch).execute()

print(f"{len(data_list)} registros insertados correctamente.")
    