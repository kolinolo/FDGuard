from Objetos import *
import os

cwd = os.getcwd()
raiz = configs['raizPastas']


def difPastas(de, para):

    adicionar = []
    remover = []
    antigo = [p.name for p in  Path(f"{cwd}/{de}").iterdir()]
    novo = [p.name for p in  Path(f"{cwd}/{para}").iterdir()]


    for p in novo:
        if p not in antigo:
            adicionar.append(p)

    for p in antigo:
        if p not in novo:
            remover.append(p)
    return {'add': adicionar, 'rmv': remover}


def transformar(req:TransformRequest):


    pastaAtual = fr'{raiz}\{req.tributacao}\Clientes ativos\{req.label}'
    pastaAlvo = fr'{raiz}\{req.tributacaoAlvo}\Clientes ativos\{req.label}'


    #Limpa arquivos indesejados da pasta
    for nome in ("Thumbs.db", ".DS_Store"):
        for arq in Path(pastaAtual).rglob(nome):
            arq.unlink(missing_ok=True)


    shutil.move(pastaAtual, pastaAlvo)




def mover(req):

    pass