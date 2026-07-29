from fastapi import FastAPI
app = FastAPI(title="minha primeira API")

@app.get('/')
def principal():
    return {'mensagem': 'Minha primeira API em FastAPI!'}

@app.get('/sobre')
def sobre():
    return {'mensagem': 'Pagina sobre'}