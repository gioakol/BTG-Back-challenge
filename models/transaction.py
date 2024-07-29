from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_id():
    return str(uuid4())

def generate_date():
    return str(datetime.now())

class Transaction(BaseModel):
    idTransaction: str = Field(default_factory=generate_id)
    idClient: str
    idFund: str
    transactionDate: str = Field(default_factory=generate_date)
    isCanceled: bool = False