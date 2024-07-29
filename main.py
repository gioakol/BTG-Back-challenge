from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import routes_transactions, routes_clients, routes_funds, routes_clientsTransactions, routes_email
from database.db import Validate_Schema

app = FastAPI()

# Configuración de CORS
origins = [
    getenv("AWS_MAIL_TOPIC_ARN")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creación routing
app.include_router(routes_clients, prefix="/clients")
app.include_router(routes_funds, prefix="/funds")
app.include_router(routes_transactions, prefix="/transactions")
app.include_router(routes_clientsTransactions, prefix="/clientsTransactions")
app.include_router(routes_email, prefix="/email")

# Validación objetos de base de datos DynamoBD
Validate_Schema()