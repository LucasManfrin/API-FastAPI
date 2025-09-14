from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

# Criar a conexao com o banco de dados
db = create_engine("sqlite:///database/banco.db")

# Criar a base do banco de dados
Base = declarative_base()

# Criar as classes/tabelas do banco
"""Tabela usuario"""
class Usuario(Base):
    __tablename__ = "usuarios"

    """Campos da tabela"""
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo = True, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

"""Tabela pedidos"""
class Pedido(Base):
    __tablename__ = "pedidos"

    # status_pedidos = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "PENDENTE"),
    # )

    """Campos da tabela"""
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) 
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        # percorrer todos os itens do pedido
        # somar todos os precos de todos os itens dos pedidos
        # editar no campo "preco" o valor final do preco do pedido
        
        # preco_pedido = 0
        # for item in self.itens:
        #     preco_item = item.preco_unitario * item.quantidade
        #     preco_pedido += preco_item
        # self.preco = preco_pedido
        
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens) # list comprehension

"""Tabela ItensPedido"""
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    """Campos da tabela"""
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidae", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

# Executar a criacao dos metadados do banco (cria efetivamente o banco)