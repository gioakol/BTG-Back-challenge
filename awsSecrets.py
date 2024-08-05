from os import getenv
import json
import boto3
from dotenv import load_dotenv, set_key


def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name=getenv("REGION_NAME"),
                          aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'))

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = response['SecretString']
        return json.loads(secret)
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None


def update_env_file(dotenv_path='.env'):
    secret_name = 'btg-challenge-secrets' 
    secrets = get_secret(secret_name)
    
    if secrets is None:
        print("No se pudo recuperar los secretos.")
        return

    load_dotenv(dotenv_path)

    set_key(dotenv_path, 'CORS_ORIGIN', secrets.get('CORS_ORIGIN', ''))
    set_key(dotenv_path, 'AWS_MAIL_TOPIC_ARN', secrets.get('AWS_MAIL_TOPIC_ARN', ''))

    print(".env actualizado con secretos.")
