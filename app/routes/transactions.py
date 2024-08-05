from fastapi import APIRouter
from app.database.transactions import createTransaction, updateTransaction
from app.models.transaction import Transaction

routes_transactions = APIRouter()


@routes_transactions.post("/subscribe", response_model=Transaction)
def suscribe(transaction: Transaction):
    return createTransaction(transaction)


@routes_transactions.put("/unscribe", response_model=Transaction)
def unscribe(transaction: Transaction):
    return updateTransaction(transaction)
