import os
import boto3
from datetime import datetime

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
BUCKET_NAME = "mlopsprojecbck"
REPORT_FOLDER = "reportes"

def log_prediction_to_s3(prediction: str, environment: str):
    filename = f"predicciones_{environment}.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"{timestamp} - {prediction} - {environment}\n"

    s3 = boto3.client("s3",
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)

    key = f"{REPORT_FOLDER}/{filename}"

    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        previous_content = obj['Body'].read().decode('utf-8')
    except s3.exceptions.NoSuchKey:
        previous_content = ""

    new_content = previous_content + content

    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=new_content.encode('utf-8'))