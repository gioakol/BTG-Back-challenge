from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

table = dynamodb.Table("Clients")

def getClientById(idClient: str):
    try:
        response = table.get_item(
            Key={"idClient": idClient}
        )

        if "Item" not in response:
            return JSONResponse(content={"message": "El cliente al que intenta acceder no se encuentra."}, status_code=404)

        return response["Item"]    
    except ClientError as ex:
        return JSONResponse(content = ex.response["Error"], status_code = 500)
