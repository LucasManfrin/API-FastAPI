from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
# from fastapi.middleware.cors import CORSMiddleware  HABILITAR QUANDO FOR INTEGRAR O FRONT

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALOGORITHM = os.getenv("ALOGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

# origins = [
#     "http://localhost:3000",  # Endereço do seu frontend React
#     "http://127.0.0.1:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
#     allow_headers=["*"],  # Permite todos os headers
# )

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from routes.auth_routes import auth_router
from routes.order_routes import order_router


app.include_router(auth_router)
app.include_router(order_router)
