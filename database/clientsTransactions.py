from .transactions import getTransactionsByIdClient
from .funds import getAllFunds
from .clients import getClientById
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from decimal import Decimal



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

        investedAmount = getInvestedAmountByClient(transactions_data)
        
        amount = client_data.get('amount', 0.0)
        if isinstance(amount, Decimal):
            amount = float(amount)
        
        avaiableAmount = amount - float(investedAmount)
        
        client_data["avaiableAmount"] = avaiableAmount
        client_data["investedAmount"] = investedAmount
        client_data["transactions"] = transactions_data

        return client_data
    
    except ClientError as ex:
        return JSONResponse(content=ex.response["Error"], status_code=500)
    

# Calculate the amount that the client has invested.
#
# Parameters:
# * transactions_data (list): List of all transactions by the client.
#
# Returns:
# * int: The total invested amount by the client.
# * JSONResponse: Error response with status code 500 if an exception occurs.
def getInvestedAmountByClient(transactions_data: dict):
    try:
        investedAmount = 0.0  # Inicializar como float

        if not isinstance(transactions_data, list):
            return JSONResponse(content={"message": "Se ha detectado un error obteniendo la información de las transacciones para calcular el monto invertido por el cliente."}, status_code=500)
        
        for transaction in transactions_data:
            amount = transaction.get('investedAmount')
            if isinstance(amount, Decimal):
                amount = float(amount)  # Convertir Decimal a float
            if isinstance(amount, (float, int)):
                investedAmount += amount

        return investedAmount    
    except ClientError as ex:
        return JSONResponse(content=ex.response["Error"], status_code=500)
    