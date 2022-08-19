from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def init_req():
    return {'Hello': 'World'}
