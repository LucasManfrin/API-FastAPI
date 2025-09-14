from sqlalchemy.orm import sessionmaker, Session
from database.models import db, Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALOGORITHM, oauth2_schema

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session

    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    # verificar se o token e valido e extrarir o ID do usuario do token
    try: 
        dic_info = jwt.decode(token, SECRET_KEY, ALOGORITHM)
        id_usuario = int(dic_info.get("sub"))

    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Invalido")
    return usuario