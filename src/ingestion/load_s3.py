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
BUCKET_NAME = "perabank-data-bucket-1634864163"  # Cambia esto por el nombre de tu bucket
upload_to_s3("data/outputs/data_s3.csv", BUCKET_NAME, "data/data_perabank_s3.csv")