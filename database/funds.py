from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

table = dynamodb.Table("Funds")

def getAllFunds():
    try:
        response = table.scan()

        return response["Items"]
    except ClientError as ex:
        return JSONResponse(content = ex.response["Error"], status_code = 500)

def getFundById(idFund: str):
    try:
        response = table.get_item(
            Key={"idFund": idFund}
        )

        if "Item" not in response:
            return JSONResponse(content={"message": "El fondo al que intenta acceder no se encuentra."}, status_code=404)

        return response["Item"]    
    except ClientError as ex:
        return JSONResponse(content = ex.response["Error"], status_code = 500)

