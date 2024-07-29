from fastapi import APIRouter
from database.clientsTransactions import getAllInfoClientById
from models.transaction import Transaction

routes_clientsTransactions = APIRouter()


@routes_clientsTransactions.get("/getAll/{idClient}")
def getAllByClientId(idClient: str):
    return getAllInfoClientById(idClient, True)


@routes_clientsTransactions.get("/getAllActive/{idClient}")
def getAllActiveByClientId(idClient: str):
    return getAllInfoClientById(idClient, False)
