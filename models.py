from sqlalchemy import Column, Integer, String, Float
from database import Base
class ProdutoDB(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    
class PetsDB(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    especie = Column(String(100), nullable=False)
    raca = Column(String(100), nullable=False)
    idade = Column(Float, nullable=False)