from fastapi import APIRouter
from app.database.clientsTransactions import getAllInfoClientById
from app.models.transaction import Transaction

routes_clientsTransactions = APIRouter()


@routes_clientsTransactions.get("/getAll/{idClient}")
def getAllByClientId(idClient: str):
    return getAllInfoClientById(idClient, True)


@routes_clientsTransactions.get("/getAllActive/{idClient}")
def getAllActiveByClientId(idClient: str):
    return getAllInfoClientById(idClient, False)
