import json
import os
import subprocess
from pathlib  import Path
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Exceptions import *

from Operations import *


def set_acl(path, group, permissions):

    # ACL atual — recursiva
    subprocess.run([
        "setfacl",
        "-R",
        "-m",
        f"g:{group}:{permissions}",
        path
    ], check=True)

    # ACL padrão — somente no diretório raiz
    subprocess.run([
        "setfacl",
        "-d",
        "-m",
        f"g:{group}:{permissions}",
        f"{path}/"
    ], check=True)



def acls(caminho):

    if os.name != 'nt':
        print(f'Adicionando permições: {caminho}\n')

        for grupo in configs['permissoes']:

            print(f"\t{grupo}", f"\t{configs['permissoes'][grupo]}")

            for subF in os.listdir(Path(caminho)):


                try:
                    set_acl(f"{caminho}/{subF}",grupo,configs['permissoes'][grupo])
                except Exception as e:
                    print(f'Erro ao impor ACLs:\n {e}')
    else:
        print('Sistema Windows, ignorando os ACLs')

app = FastAPI()

# Habilita CORS para permitir que JS no navegador acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique a origem do front-end
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)



meses = [f'0{m}'[-2:] for m in range(1, 13)]

with open("configs.json", "r", encoding="utf-8") as file: configs = json.load(file)



class npRequest (BaseModel):

    nome: str
    tributacao: str
    contabilidadeA: bool





@app.post('/novaPasta', methods=['POST'])
def NovaPastaEndPoint (novaPasta:npRequest):
    return novaPasta(novaPasta)


@app.post('/moverPasta', methods=['POST'])
def moverPasta():



    pass








if __name__ == "__main__":  # Caso seja a primeira função chamada, executa o servidor com uvicorn na porta 80000
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=81)
