from .db import dynamodb
from .funds import getFundById
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from models.transaction import Transaction
from utils.mailSender import sendMailNotificationSubscribe
from decimal import Decimal

table = dynamodb.Table("Transactions")



# Create a new transaction.
#
# Parameters:
# * data (Transaction): The transaction data to be created.
#
# Returns:
# * JSONResponse: Success message if the transaction is created successfully, or an error message if there are insufficient funds or if a server error occurs.
def createTransaction(data: Transaction):
    try:
        from .clientsTransactions import getAllInfoClientById

        idClient = str(data.idClient)
        idFund = str(data.idFund)

        print(1)
        client_data = getAllInfoClientById(idClient, False)
        fund_data = getFundById(idFund)
        
        print(2)
        avaiableAmount = client_data.get('avaiableAmount', 0)
        
        if data.investedAmount <= avaiableAmount: 
            print(3)
            print(data.investedAmount)

            transaction = data.dict()
            table.put_item(Item=transaction)

            res = sendMailNotificationSubscribe(client_data.get('fullName', 0), client_data.get('email', 0), client_data.get('phone', 0), fund_data.get('category', 0), fund_data.get('name', 0), "subscribed")
                
            if res == True:
                return JSONResponse(content={"message": f"Se ha suscrito exitosamente al {"Fondo voluntario de pensión" if fund_data.get('category', 0) == "FPV" else "Fondo de inversión colectiva"} '{fund_data.get('name', 0)}', se te ha enviado un correo con la confirmación de la transacción."}, status_code=200)
            else:
                return JSONResponse(content={"message": f"Se ha suscrito exitosamente al {"Fondo voluntario de pensión" if fund_data.get('category', 0) == "FPV" else "Fondo de inversión colectiva"} '{fund_data.get('name', 0)}', no hemos podido enviarte un correo con la confirmación de la transacción."}, status_code=200)
        else:
            print(4)
            return JSONResponse(content={"message": f"No tiene saldo disponible para vincularse al {"Fondo voluntario de pensión" if fund_data.get('category', 0) == "FPV" else "Fondo de inversión colectiva"} '{fund_data.get('name', 0)}'."}, status_code=401)
    except ClientError as ex:
        return JSONResponse(content=ex.response["Error"], status_code=500)
    

# Update an existing transaction.
#
# Parameters:
# * data (Transaction): The transaction data to be updated.
#
# Returns:
# * JSONResponse: Success message if the transaction is updated successfully, or an error message if the transaction is not found or if a server error occurs.
def updateTransaction(data: Transaction):
    try:
        from .clientsTransactions import getAllInfoClientById

        idClient = str(data.idClient)
        idFund = str(data.idFund)

        client_data = getAllInfoClientById(idClient, True)
        fund_data = getFundById(idFund)

        transactionsActive = getTransactionsByIdClientByIsCanceled(idClient, idFund, False)

        if len(transactionsActive) > 0:
            transaction_item = transactionsActive[0]
                            
            table.update_item(
                Key={"idTransaction": transaction_item["idTransaction"]},
                UpdateExpression="set isCanceled = :c",
                ExpressionAttributeValues={":c": True}
            )

            res = sendMailNotificationSubscribe(client_data.get('fullName', 0), client_data.get('email', 0), client_data.get('phone', 0), fund_data.get('category', 0), fund_data.get('name', 0), "subscribed")
            
            if res == True:
                return JSONResponse(content={"message": f"Se ha dado de baja exitosamente al {"Fondo voluntario de pensión" if fund_data.get('category', 0) == "FPV" else "Fondo de inversión colectiva"} '{fund_data.get('name', 0)}', se te ha enviado un correo con la confirmación de la transacción."}, status_code=200)
            else:
                return JSONResponse(content={"message": f"Se ha dado de baja exitosamente al {"Fondo voluntario de pensión" if fund_data.get('category', 0) == "FPV" else "Fondo de inversión colectiva"} '{fund_data.get('name', 0)}', no hemos podido enviarte un correo con la confirmación de la transacción."}, status_code=200)
        else:
            return JSONResponse(content={"message": f"La transacción del {"Fondo voluntario de pensión" if fund_data.get('category', 0) == "FPV" else "Fondo de inversión colectiva"} '{fund_data.get('name', 0)}' no se encuentra disponible."}, status_code=404)
    except ClientError as ex:
        return JSONResponse(content={"error": str(ex)}, status_code=500)


# Retrieve transactions by client ID.
#
# Parameters:
# * idClient (str): The unique identifier of the client.
# * allTransactions (bool): When True, retrieves all transactions. When False, retrieves only active transactions.
#
# Returns:
# * list: A list of transactions for the specified client.
# * JSONResponse: Error response with status code 500 if a server error occurs.
def getTransactionsByIdClient(idClient: str, allTransactions: bool):
    try:
        key_condition = Key("idClient").eq(idClient)

        if allTransactions == False:
            filter_expression = Attr("isCanceled").eq(False)

            response = table.query(
                IndexName="ClientIndex",
                KeyConditionExpression=key_condition,
                FilterExpression=filter_expression
            )
        else:
            response = table.query(
                IndexName="ClientIndex",
                KeyConditionExpression=key_condition
            )
            
        return response["Items"]    
    except ClientError as ex:
        return JSONResponse(content=ex.response["Error"], status_code=500)


# Retrieve transactions by client ID and cancellation status.
#
# Parameters:
# * idClient (str): The unique identifier of the client.
# * idFund (str): The unique identifier of the fund.
# * isCanceled (bool): The cancellation status of the transaction.
#
# Returns:
# * list: A list of transactions for the specified client and fund with the given cancellation status.
# * JSONResponse: Error response with status code 500 if a server error occurs.
def getTransactionsByIdClientByIsCanceled(idClient: str, idFund: str, isCanceled: bool):
    try:
        response = table.query(
            IndexName='ClientIndex',
            KeyConditionExpression=Key('idClient').eq(idClient),
            FilterExpression=Attr('idFund').eq(idFund) & Attr('isCanceled').eq(isCanceled)
        )
            
        return response["Items"]    
    except ClientError as ex:
        return JSONResponse(content=ex.response["Error"], status_code=500)
