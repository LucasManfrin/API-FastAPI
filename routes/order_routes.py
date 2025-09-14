from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from database.schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from database.models import Pedido, Usuario, ItemPedido
from typing import List

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """
    Lugar para realizar a explicacao...
    """
    return {
            "mensagem": "Voce acessou a rota de pedidos"
            }

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)): 
    novo_pedido = Pedido(usuario = pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem:", f"Pedido criado com sucesso. Id do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para cancelar pedido """
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido numero :{pedido.id} cancelado com sucesso",  # chamando o id dentro do pedido (pedido.id e nao pegando do id_pedido) faz com que o fastapi carregue todas as infos
        "pedido": pedido                                                  # do pedido (lazy loaded, carregamento preguicoso)
    }
 
@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para realizar essa operacao")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }
    
@order_router.post("/pedido/adicionar_item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco() # editando o campo preco desse pedido
    session.commit()
    return {
        "mensagem": "Item criado com sucesso",
        "pedido_id": pedido.id,
        "item_id": item_pedido.id,
        "pedido": pedido
    }

@order_router.post("/pedido/remover_item/{id_item_pedido}")
async def remover(id_item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
    session.delete(item_pedido)
    pedido.calcular_preco() # editando o campo preco desse pedido
    session.commit()
    return {
        "mensagem": "Item removido com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# finalizar um pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Rota para cancelar pedido """
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"Pedido numero:{pedido.id} finalizado com sucesso",  # chamando o id dentro do pedido (pedido.id e nao pegando do id_pedido) faz com que o fastapi carregue todas as infos
        "pedido": pedido                                                  # do pedido (lazy loaded, carregamento preguicoso)
    }

# visualizar 1 pedido
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa modificacao")    
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# visualizar todos os pedidos de 1 usuario
@order_router.get("/listar/{id_usuario}", response_model=List[ResponsePedidoSchema])
async def listar_pedidos_usuario(id_usuario: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para realizar essa operacao")
    else:
        pedidos = session.query(Pedido).filter(Pedido.usuario == id_usuario).all()
        return pedidos