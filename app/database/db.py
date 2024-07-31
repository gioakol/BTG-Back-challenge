from connection import dynamodb

from botocore.exceptions import ClientError
from decimal import Decimal



# Check if a table exists in DynamoDB.
#
# Parameters:
# * table_name (str): The name of the table to check.
#
# Returns:
# * bool: True if the table exists, False otherwise.
def table_exists(table_name):
    
    try:
        table = dynamodb.Table(table_name)
        table.load()
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        else:
            raise e

# Create table Clients in DynamoDB.
#
# Parameters:
#
# Returns:
# * bool: True if the table was created, False otherwise.
def Create_Table_Clients():
    result = False

    try:

        clients_table = dynamodb.create_table(
            TableName='Clients',
            KeySchema=[
                {
                    'AttributeName': 'idClient',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'idClient',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

        clients_table.meta.client.get_waiter('table_exists').wait(TableName='Clients')
        result = True

    except Exception as e:
        print("There was an error creating the table Clients: " + str(e))
    
    return result

# Insert default rows in table Clients.
#
# Parameters:
#
# Returns:
# * bool: True if the table was created, False otherwise.
def Insert_Table_Clients():
    result = False

    try:
        clients_table = dynamodb.Table('Clients')
        
        clients = {
            'idClient': '1', 
            'fullName': 'Giovanni Beltran Avila', 
            'email': 'gioakol@gmail.com',
            'phone': '+57 3229702531',
            'amount': 500000
        }

        clients_table.put_item(Item=clients)
        result = True

    except Exception as e:
        print("An error occurred updating the table Clients: " + str(e))

    return result

# Create table Funds in DynamoDB.
#
# Parameters:
#
# Returns:
# * bool: True if the table was created, False otherwise.
def Create_Table_Funds():
    result = False

    try:
        funds_table = dynamodb.create_table(
            TableName='Funds',
            KeySchema=[
                {
                    'AttributeName': 'idFund',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'idFund',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

        funds_table.meta.client.get_waiter('table_exists').wait(TableName='Funds')
        result = True

    except Exception as e:
        print("There was an error creating the table Funds: " + str(e))

    return result

# Insert default rows in table Funds.
#
# Parameters:
#
# Returns:
# * bool: True if the table was created, False otherwise.
def Insert_Table_Funds():
    result = False
    
    try: 
        funds_table = dynamodb.Table('Funds')

        funds = [
            {"idFund": "1", "name": "FPV_BTG_PACTUAL_RECAUDADORA", "minimumAmount": Decimal('75000'), "category": "FPV"},
            {"idFund": "2", "name": "FPV_BTG_PACTUAL_ECOPETROL", "minimumAmount": Decimal('125000'), "category": "FPV"},
            {"idFund": "3", "name": "DEUDAPRIVADA", "minimumAmount": Decimal('50000'), "category": "FIC"},
            {"idFund": "4", "name": "FDO-ACCIONES", "minimumAmount": Decimal('250000'), "category": "FIC"},
            {"idFund": "5", "name": "FPV_BTG_PACTUAL_DINAMICA", "minimumAmount": Decimal('100000'), "category": "FPV"}
        ]

        for fund in funds:
            funds_table.put_item(Item=fund)
        result = True

    except Exception as e:
        print("An error occurred updating the table Funds: " + str(e))

    return result

# Create table Transactions in DynamoDB.
#
# Parameters:
#
# Returns:
# * bool: True if the table was created, False otherwise.
def Create_Table_Transactions():
    result = False

    try:
        transactions_table = dynamodb.create_table(
            TableName='Transactions',
            KeySchema=[
                {
                    'AttributeName': 'idTransaction',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'idTransaction',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'idClient',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'idFund',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'transactionDate',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'ClientIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'idClient',
                            'KeyType': 'HASH'  # Partition key
                        },
                        {
                            'AttributeName': 'transactionDate',
                            'KeyType': 'RANGE'  # Sort key
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10
                    }
                },
                {
                    'IndexName': 'FundIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'idFund',
                            'KeyType': 'HASH'  # Partition key
                        },
                        {
                            'AttributeName': 'transactionDate',
                            'KeyType': 'RANGE'  # Sort key
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        
        transactions_table.meta.client.get_waiter('table_exists').wait(TableName='Transactions')
        result = True

    except Exception as e:
        print("There was an error creating the table Transactions: " + str(e))

    return result

# Check if a table exists in DynamoDB.
#
# Parameters:
#
# Returns:
# 
def Validate_Schema():
    
    existTables = (table_exists("Clients")) and (table_exists("Funds")) and (table_exists("Transactions"))

    if not existTables:
        if not table_exists("Clients"):
            res = Create_Table_Clients()
            if res:
                Insert_Table_Clients()
        if not table_exists("Funds"):
            res = Create_Table_Funds()
            if res:
                Insert_Table_Funds()
        if not table_exists("Transactions"):
            res = Create_Table_Transactions()
    #else:
    #    print('Schema updated')
