
from fastapi import APIRouter
from database.funds import getAllFunds

routes_funds = APIRouter()

@routes_funds.get("/getAll")
def getAll():
    return getAllFunds()