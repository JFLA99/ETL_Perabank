import pandas as pd
import os
import boto3
from botocore.exceptions import NoCredentialsError

# Ruta al archivo fuente
DATA_PATH = "data/bank-additional-full.csv"

# Cargar el dataset completo
df = pd.read_csv(DATA_PATH, sep=';')

# Partir en 60% / 20% / 20%
df_rds = df.sample(frac=0.6, random_state=42)              # 60% de los datos en la RDS
df_remaining = df.drop(df_rds.index)
df_local = df_remaining.sample(frac=0.5, random_state=42)  # 20% de los datos en local
df_s3 = df_remaining.drop(df_local.index)                  # 20% de los datos en S3

# Crear carpeta si no existe
os.makedirs("data/outputs", exist_ok=True)

# Guardar
df_local.to_csv("data/outputs/data_local.csv", index=False)
df_s3.to_csv("data/outputs/data_s3.csv", index=False)
df_rds.to_csv("data/outputs/data_rds.csv", index=False)


# Subir a S3
def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True


# Subir el dataset a S3 
BUCKET_NAME = "Perabank_s3_EIA"  # Cambia esto por el nombre de tu bucket
upload_to_s3("data/outputs/data_s3.csv", BUCKET_NAME, "data/data_perabank_s3.csv")
