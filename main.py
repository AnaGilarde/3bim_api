from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import ProdutoDB
from models import PetsDB
from schemas import ProdutoCreate, ProdutoResponse
from schemas import PetsCreate, PetsResponse
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine) # cria as tabelas, se ainda não existirem
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # em produção, restringir para o domínio real do front-end
    allow_methods=['*'],
    allow_headers=['*'],
 )

 def buscar_produto(db: Session, produto_id: int):
    return db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()

@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()

@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

# GET /produtos/{id} -> retorna um único produto pelo id
@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
   produto = buscar_produto(db, produto_id)
    if produto is None: raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto

# DELETE /produtos/{id} -> remove um produto do banco de dados
@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
 produto = buscar_produto(db, produto_id)
 if produto is None:
     raise HTTPException(status_code=404, detail='Produto não encontrado')
 db.delete(produto)
 db.commit()

# main.py (trecho adicionado)
from fastapi import HTTPException
# GET /produtos/{id} -> consulta um produto pelo id no banco
@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
 produto = buscar_produto(db, produto_id)
 if produto is None:
     raise HTTPException(status_code=404, detail='Produto nãoencontrado')
 return produto
# DELETE /produtos/{id} -> remove um produto do banco
@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
 produto = buscar_produto(db, produto_id)
 if produto is None:
      raise HTTPException(status_code=404, detail='Produto não encontrado')
 db.delete(produto)
 db.commit()

# PUT /produtos/{id} -> atualiza um produto existente no banco
@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoCreate, db:
Session = Depends(get_db)):
 produto = buscar_produto(db, produto_id)
 if produto is None:
     raise HTTPException(status_code=404, detail='Produto não encontrado')
 produto.nome = dados.nome
 produto.preco = dados.preco
 produto.quantidade = dados.quantidade
 db.commit()
 db.refresh(produto)
 return produto



@app.get('/pets', response_model=list[PetsResponse])
def listar_pets(db: Session = Depends(get_db)):
    return db.query(PetsDB).all()

@app.post('/pets', response_model=PetsResponse, status_code=201)
def criar_pet(pets: PetsCreate, db: Session = Depends(get_db)):
    novo_pets = PetsDB(**pets.dict())
    db.add(novo_pets)
    db.commit()
    db.refresh(novo_pets)
    return novo_pets

# GET /produtos/{id} -> retorna um único produto pelo id
@app.get('/pets/{pets_id}', response_model=PetsResponse)
def obter_pet(pets_id: int, db: Session = Depends(get_db)):
    pets = db.query(PetsDB).filter(PetsDB.id ==pets_id).first()
    if pets is None: raise HTTPException(status_code=404, detail='Pets não encontrado')
    return pets

# DELETE /produtos/{id} -> remove um produto do banco de dados
@app.delete('/pets/{pets_id}', status_code=204)
def remover_pet(pets_id: int, db: Session = Depends(get_db)):
 pets = db.query(PetsDB).filter(PetsDB.id ==pets_id).first()
 if pets is None:
     raise HTTPException(status_code=404, detail='Pets não encontrado')
 db.delete(pets)
 db.commit()

# main.py (trecho adicionado)
from fastapi import HTTPException
# GET /produtos/{id} -> consulta um produto pelo id no banco
@app.get('/pets/{pets_id}', response_model=PetsResponse)
def obter_pet(pets_id: int, db: Session = Depends(get_db)):
 pet = db.query(PetsDB).filter(PetsDB.id ==pets_id).first()
 if pet is None:
     raise HTTPException(status_code=404, detail='Pets não encontrado')
 return pet
# DELETE /produtos/{id} -> remove um produto do banco
@app.delete('/pets/{pets_id}', status_code=204)
def remover_produto(pets_id: int, db: Session = Depends(get_db)):
 pets = db.query(PetsDB).filter(PetsDB.id ==pets_id).first()
 if pets is None:
      raise HTTPException(status_code=404, detail='Pets não encontrado')
 db.delete(pets)
 db.commit()

# PUT /produtos/{id} -> atualiza um produto existente no banco
@app.put('/pets/{pets_id}', response_model=PetsResponse)
def atualizar_pet(pets_id: int, dados: PetsCreate, db:
Session = Depends(get_db)):
 pets = db.query(PetsDB).filter(PetsDB.id == pets_id).first()
 if pets is None:
     raise HTTPException(status_code=404, detail='Pets não encontrado')
 pets.nome = dados.nome
 pets.especie = dados.especie
 pets.raca = dados.raca
 pets.idade = dados.idade
 db.commit()
 db.refresh(pets)
 return pets

