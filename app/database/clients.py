from app.database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from fastapi import HTTPException


table = dynamodb.Table("Clients")



# Retrieve client data by client ID.
#
# Parameters:
# * idClient (str): The unique identifier of the client.
#
# Returns:
# * dict: Client data if found.
# * JSONResponse: Error response with status code 404 if the client is not found, or 500 if a server error occurs.
def getClientById(idClient: str):
    try:
        response = table.get_item(
            Key={"idClient": idClient}
        )

        if "Item" not in response:
            return JSONResponse(content={"message": "El cliente al que intenta acceder no se encuentra."}, status_code=404)

        return response["Item"]    
    except ClientError as ex:
        raise HTTPException(status_code=500, detail="Internal Server Error")
