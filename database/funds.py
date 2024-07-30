from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

table = dynamodb.Table("Funds")


# Retrieve all funds information.
#
# Parameters:
# None
#
# Returns:
# * list: A list of dictionaries containing data for all funds.
# * JSONResponse: Error response with status code 500 if a server error occurs.
def getAllFunds():
    try:
        response = table.scan()

        return response["Items"]
    except ClientError as ex:
        return JSONResponse(content = ex.response["Error"], status_code = 500)


# Retrieve fund information by fund ID.
#
# Parameters:
# * idFund (str): The unique identifier of the fund.
#
# Returns:
# * dict: Fund data if found.
# * JSONResponse: Error response with status code 404 if the fund is not found, or 500 if a server error occurs.
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

