from pydantic import BaseModel
from typing import Optional, List


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True 

class PedidoSchema(BaseModel): 
    id_usuario: int

    class config:
        from_attributos = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class config:
        from_attributos = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class config:
        from_attributos = True

class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]

    class config:
        from_attributos = True
