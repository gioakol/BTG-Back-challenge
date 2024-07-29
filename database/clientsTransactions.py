from .transactions import getTransactionsByIdClient
from .funds import getAllFunds
from .clients import getClientById
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse



# Get all information from client (with transactions and amounts)
#
# Parameters:
# * idClient (str): The unique identifier of the client from the table.
# * allTransactions (bool): When True, retrieves all transactions. When False, retrieves only active transactions.
#
# Returns:
# * dict: Client data including transactions data, available amount, and invested amount.
# * JSONResponse: Error response with status code 500 if an exception occurs.
def getAllInfoClientById(idClient: str, allTransactions: bool):
    try:
        client_data = getClientById(idClient)
        
        transactions_data = getTransactionsByIdClient(idClient, allTransactions)

        funds_data = getAllFunds()

        investedAmount = getInvestedAmountByClient(funds_data, transactions_data)
        avaiableAmount = client_data.get('amount', 0) - investedAmount
        
        client_data["avaiableAmount"] = avaiableAmount
        client_data["investedAmount"] = investedAmount
        client_data["transactions"] = transactions_data
        
        return client_data
    
    except ClientError as ex:
        return JSONResponse(content=ex.response["Error"], status_code=500)
    

# Calculate the amount that the client has invested.
#
# Parameters:
# * funds_data (list): List of all funds information.
# * transactions_data (list): List of all transactions by the client.
#
# Returns:
# * int: The total invested amount by the client.
# * JSONResponse: Error response with status code 500 if an exception occurs.
def getInvestedAmountByClient(funds_data: dict, transactions_data: dict):
    try:
        investedAmount = 0

        if not isinstance(funds_data, list):
            return JSONResponse(content={"message": "Se ha detectado un error obteniendo la información de los fondos para calcular el monto invertido por el cliente."}, status_code=500)
        
        funds = {fund['idFund']: fund['minimumAmount'] for fund in funds_data}

        if not isinstance(transactions_data, list):
            return JSONResponse(content={"message": "Se ha detectado un error obteniendo la información de las transacciones para calcular el monto invertido por el cliente."}, status_code=500)
        
        fund_ids = {transaction['idFund'] for transaction in transactions_data}
        
        for fund_id in fund_ids:
            if fund_id in funds:
                investedAmount += funds[fund_id]

        return investedAmount
    
    except ClientError as ex:
        return JSONResponse(content=ex.response["Error"], status_code=500)
