from os import getenv
import boto3
from dotenv import load_dotenv
from boto3 import resource

load_dotenv()


sns_client = boto3.client("sns",  
                          aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
                          region_name=getenv("REGION_NAME"))


dynamodb = resource("dynamodb",
                    aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
                    region_name=getenv("REGION_NAME"))
