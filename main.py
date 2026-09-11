from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import ProdutoDB, PetsDB
from schemas import ProdutoCreate, ProdutoResponse
from schemas import PetsCreate, PetsResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


@app.on_event("startup")
def criar_tabelas():
    Base.metadata.create_all(bind=engine)


def buscar_produto(db: Session, produto_id: int):
    return db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()


@app.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()


@app.post("/produtos", response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@app.get("/produtos/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = buscar_produto(db, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto


@app.delete("/produtos/{produto_id}", status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = buscar_produto(db, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    db.delete(produto)
    db.commit()


@app.put("/produtos/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoCreate,
    db: Session = Depends(get_db)
):
    produto = buscar_produto(db, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    for campo, valor in dados.dict().items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto

@app.get("/pets", response_model=list[PetsResponse])
def listar_pets(db: Session = Depends(get_db)):
    return db.query(PetsDB).all()


@app.post("/pets", response_model=PetsResponse, status_code=201)
def criar_pets(
    pets: PetsCreate,
    db: Session = Depends(get_db)
):
    novo_pets = PetsDB(**pets.dict())

    db.add(novo_pets)
    db.commit()
    db.refresh(novo_pets)

    return novo_pets


@app.get("/pets/{pets_id}", response_model=PetsResponse)
def obter_pets(
    pets_id: int,
    db: Session = Depends(get_db)
):
    pets = (
        db.query(PetsDB)
        .filter(PetsDB.id == pets_id)
        .first()
    )

    if pets is None:
        raise HTTPException(
            status_code=404,
            detail="Pet não encontrado"
        )

    return pets


@app.delete("/pets/{pets_id}", status_code=204)
def remover_pets(
    pets_id: int,
    db: Session = Depends(get_db)
):
    pets = (
        db.query(PetsDB)
        .filter(PetsDB.id == pets_id)
        .first()
    )

    if pets is None:
        raise HTTPException(
            status_code=404,
            detail="Pet não encontrado"
        )

    db.delete(pets)
    db.commit()


@app.put("/pets/{pets_id}", response_model=PetsResponse)
def atualizar_pets(
    pets_id: int,
    dados: PetsCreate,
    db: Session = Depends(get_db)
):
    pets = (
        db.query(PetsDB)
        .filter(PetsDB.id == pets_id)
        .first()
    )

    if pets is None:
        raise HTTPException(
            status_code=404,
            detail="Pet não encontrado"
        )

    pets.nome = dados.nome

    db.commit()
    db.refresh(pets)

    return pets