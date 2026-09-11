from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_db
from models import ProdutoDB, PetsDB

client = TestClient(app)


def test_listar_produtos_com_mock():
    db_mock = MagicMock()

    db_mock.query.return_value.all.return_value = [
        ProdutoDB(
            id=1,
            nome="Teclado",
            preco=89.90,
            quantidade=15
        )
    ]

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get("/produtos")

    assert resposta.status_code == 200
    assert resposta.json()[0]["nome"] == "Teclado"

    app.dependency_overrides.clear()


def test_criar_produto_com_mock():
    db_mock = MagicMock()

    def simular_refresh(produto):
        produto.id = 1

    db_mock.refresh.side_effect = simular_refresh

    app.dependency_overrides[get_db] = lambda: db_mock

    novo_produto = {
        "nome": "Monitor",
        "preco": 799.90,
        "quantidade": 5
    }

    resposta = client.post("/produtos", json=novo_produto)

    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Monitor"
    assert resposta.json()["id"] == 1

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()


def test_obter_produto_com_mock():
    db_mock = MagicMock()

    produto = ProdutoDB(
        id=1,
        nome="Mouse",
        preco=49.90,
        quantidade=10
    )

    db_mock.query.return_value.filter.return_value.first.return_value = produto

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get("/produtos/1")

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Mouse"
    assert resposta.json()["id"] == 1

    app.dependency_overrides.clear()


def test_remover_produto_com_mock():
    db_mock = MagicMock()

    produto = ProdutoDB(
        id=1,
        nome="Teclado",
        preco=89.90,
        quantidade=15
    )

    db_mock.query.return_value.filter.return_value.first.return_value = produto

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete("/produtos/1")

    assert resposta.status_code == 204
    db_mock.delete.assert_called_once_with(produto)
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()


def test_atualizar_produto_com_mock():
    db_mock = MagicMock()

    produto = ProdutoDB(
        id=1,
        nome="Mouse",
        preco=49.90,
        quantidade=10
    )

    db_mock.query.return_value.filter.return_value.first.return_value = produto

    app.dependency_overrides[get_db] = lambda: db_mock

    dados = {
        "nome": "Mouse Gamer",
        "preco": 99.90,
        "quantidade": 20
    }

    resposta = client.put("/produtos/1", json=dados)

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Mouse Gamer"
    assert resposta.json()["preco"] == 99.90
    assert resposta.json()["quantidade"] == 20

    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()


def test_listar_pets_com_mock():
    db_mock = MagicMock()

    db_mock.query.return_value.all.return_value = [
        PetsDB(
            id=1,
            nome="Rex",
            especie="Cachorro",
            raca="Golden Retriever",
            idade=3
        )
    ]

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get("/pets")

    assert resposta.status_code == 200
    assert resposta.json()[0]["nome"] == "Rex"

    app.dependency_overrides.clear()


def test_criar_pets_com_mock():
    db_mock = MagicMock()

    def simular_refresh(pets):
        pets.id = 1

    db_mock.refresh.side_effect = simular_refresh

    app.dependency_overrides[get_db] = lambda: db_mock

    novo_pets = {
        "nome": "Luna",
        "especie": "Gato",
        "raca": "Siamês",
        "idade": 2
    }

    resposta = client.post("/pets", json=novo_pets)

    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Luna"
    assert resposta.json()["id"] == 1

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()


def test_obter_pets_com_mock():
    db_mock = MagicMock()

    pets = PetsDB(
        id=1,
        nome="Rex",
        especie="Cachorro",
        raca="Golden Retriever",
        idade=3
    )

    db_mock.query.return_value.filter.return_value.first.return_value = pets

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get("/pets/1")

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Rex"
    assert resposta.json()["id"] == 1

    app.dependency_overrides.clear()


def test_remover_pets_com_mock():
    db_mock = MagicMock()

    pets = PetsDB(
        id=1,
        nome="Rex",
        especie="Cachorro",
        raca="Golden Retriever",
        idade=3
    )

    db_mock.query.return_value.filter.return_value.first.return_value = pets

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete("/pets/1")

    assert resposta.status_code == 204
    db_mock.delete.assert_called_once_with(pets)
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()


def test_atualizar_pets_com_mock():
    db_mock = MagicMock()

    pets = PetsDB(
        id=1,
        nome="Rex",
        especie="Cachorro",
        raca="Golden Retriever",
        idade=3
    )

    db_mock.query.return_value.filter.return_value.first.return_value = pets

    app.dependency_overrides[get_db] = lambda: db_mock

    dados = {
        "nome": "Rex Atualizado",
        "especie": "Cachorro",
        "raca": "Golden Retriever",
        "idade": 4
    }

    resposta = client.put("/pets/1", json=dados)

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Rex Atualizado"

    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()