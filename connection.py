from os import getenv
import boto3
from dotenv import load_dotenv

load_dotenv()

sns_client = boto3.client("sns",  
                          aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
                          region_name=getenv("REGION_NAME"))
