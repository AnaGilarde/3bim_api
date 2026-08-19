from pydantic import BaseModel
class ProdutoBase(BaseModel):
    nome: str
    preco: float
    quantidade: int

class ProdutoCreate(ProdutoBase):
    pass
class ProdutoResponse(ProdutoBase):
    id: int
    
class Config:
    from_attributes = True



class PetsBase(BaseModel):
    nome: str
    especie: str
    raca: str
    idade: float

class PetsCreate(PetsBase):
    pass
class PetsResponse(PetsBase):
    id: int
    
class Config:
    from_attributes = True

