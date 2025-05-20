import pandas as pd
from sqlalchemy import create_engine

# Parámetros de conexión
DB_USER = "tu_usuario"
DB_PASSWORD = "tu_contraseña"
DB_HOST = "tu_endpoint_rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "nombre_base_datos"

# Construir la URL de conexión
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Leer el CSV
df = pd.read_csv("data/outputs/data_rds.csv")

# Subir a RDS (crea o reemplaza la tabla "clientes")
df.to_sql("clientes", engine, if_exists="replace", index=False)

print("Datos subidos correctamente a RDS.")
