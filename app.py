from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Operations import *
from Objetos.reqs import *




app = FastAPI()

# Habilita CORS para permitir que JS no navegador acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique a origem do front-end
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post('/novaPasta')
def NovaPastaEndPoint (req:npRequest):

    return criarPasta(req)



@app.post('/moverPasta')
def moverPastaEndPoint(req):


    if req.op == 'transformar':

        return transformar(req)



    else:

        return mover(req)











if __name__ == "__main__":  # Caso seja a primeira função chamada, executa o servidor com uvicorn na porta 80000
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=81)
