from fastapi import APIRouter, Depends, HTTPException
from database.models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALOGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from database.schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
import pytz
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)):
    # JWT (Jason Web Tokens)
    fuso_brasilia = pytz.timezone("America/Sao_Paulo")
    data_expiracao = datetime.now(fuso_brasilia) + duracao_token

    # Convertendo datetime object para string antes 
    dic_info = {"sub": str(id_usuario), "exp": int(data_expiracao.timestamp())}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALOGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    """ Verifica se o email existe e valida se o usuario acertou a senha """
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def home():
    """
    Essa e a rota padrao para autenticacao
    """
    return {
            "mensagem": "Vc acessou a rota padrao de autenticacao",
            "autenticado": False
            }

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)): # entrada de dados do meu enpoint
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario: 
        # ja existe um usuario com esse email
        raise HTTPException(status_code=400, detail="E-mail do usuario ja cadastrado") # comeca a saida de dados do meu endpoint
    else:
        # criacao de novo usuario
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usario)
        session.commit()
        return {"mensagem": f"usuario: '{usuario_schema.nome}' cadastrado com sucesso!"}

""" login -> email e senha -> token JWT """
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado ou credenciais invalidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token = timedelta(days=7))
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
                }

@auth_router.post("/login-form")
# rota de testes dentro da documentacao do fastapi
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado ou credenciais invalidas")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token,
                "token_type": "Bearer"
                }
    
@auth_router.get("/refresh")
async def user_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {"access_token": access_token,
            "token_type": "Bearer"
            }