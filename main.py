from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import routes_transactions, routes_clients, routes_funds, routes_clientsTransactions, routes_email
from app.database.db import Validate_Schema
from awsSecrets import update_env_file

app = FastAPI()

# Configuración de CORS
origins = [
    getenv("CORS_ORIGIN")
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

# Actualización de objetos en .env
update_env_file()

# Validación objetos de base de datos DynamoBD
Validate_Schema()