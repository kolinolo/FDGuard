from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Operations import *
from Objetos import *




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



@app.post('/transformar')
def transformarPastaEndPoint(req:TransformRequest):


    if req.op == 'transformar':

        try:

            transformar(req)

            responseCode = 200
            msg = 'sucesso'

        except Exception as e:
            responseCode = 500
            msg = str(e)
    else :
        responseCode = 404
        msg = 'Not found'

    return [responseCode, msg]


@app.post('/mover')
def moverPastaEndPoint(req:MoverRequest):

    if req.op in ['transferir',
                  'inativar',
                  'baixar']:

        try:

            mover(req)

            responseCode = 200
            msg = 'sucesso'



        except Exception as e:
            responseCode = 500
            msg = str(e)

    elif req.op in ['destransferir',
                    'reativar',
                    'desbaixar']:

        try:

            mover(req,True)

            responseCode = 200
            msg = 'sucesso'

        except Exception as e:
            responseCode = 500
            msg = str(e)

    else :
        responseCode = 404
        msg = 'Not found'

    return [responseCode, msg]


@app.post('/ping')
def ping():
    return [200, 'pong']











if __name__ == "__main__":  # Caso seja a primeira função chamada, executa o servidor com uvicorn na porta 80000
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=81)
