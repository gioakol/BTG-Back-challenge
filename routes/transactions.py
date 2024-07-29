from fastapi import APIRouter
from database.transactions import createTransaction, updateTransaction
from models.transaction import Transaction

routes_transactions = APIRouter()

@routes_transactions.post("/suscribe", response_model=Transaction)
def suscribe(transaction: Transaction):
    return createTransaction(transaction)

@routes_transactions.put("/unscribe", response_model=Transaction)
def unscribe(transaction: Transaction):
    return updateTransaction(transaction)
