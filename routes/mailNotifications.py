from fastapi import APIRouter
from utils import subscribeClientMail, validateSubscribe

routes_email = APIRouter()


@routes_email.post("/subscribe/{idClient}")
def suscribe(idClient: str):
    return subscribeClientMail(idClient)


@routes_email.get("/validateSubscribe/{idClient}")
def suscribe(idClient: str):
    return validateSubscribe(idClient)
