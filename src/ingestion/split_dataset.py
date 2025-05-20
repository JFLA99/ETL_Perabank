import pandas as pd
import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
load_dotenv()

# Ruta al archivo fuente
DATA_PATH = "data/bank-additional-full.csv"

# Cargar el dataset completo
df = pd.read_csv(DATA_PATH, sep=';')

def split_dataset(df):
    """
    Divide el dataset en tres partes: 60% para RDS, 20% para almacenamiento local y 20% para S3.
    """
    # Partir en 60% / 20% / 20%
    df_rds = df.sample(frac=0.6, random_state=42)              # 60% de los datos en la RDS
    df_remaining = df.drop(df_rds.index)
    df_local = df_remaining.sample(frac=0.5, random_state=42)  # 20% de los datos en local
    df_s3 = df_remaining.drop(df_local.index)    
    
    # Crear carpeta si no existe
    os.makedirs("data/outputs", exist_ok=True)
   
    # Guardar
    df_local.to_csv("data/outputs/data_local.csv", index=False)
    df_s3.to_csv("data/outputs/data_s3.csv", index=False)
    df_rds.to_csv("data/outputs/data_rds.csv", index=False)              # 20% de los datos en S3

    return print("Dataset dividido y guardado en data/outputs")

# Llamar a la función para dividir el dataset  
split_dataset(df)


