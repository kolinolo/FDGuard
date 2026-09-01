import shutil

from Objetos import *
from Operations.ACLs import acls
import os




cwd = os.getcwd()
raiz = configs['raizPastas']
ano = configs['ano']

pastas = {

    'transferir':'Transferidos',
    'destransferir':'Transferidos',

    'inativar':'Inativos',
    'reativar':'Inativos',

    'baixar':'baixados',
    'desbaixar':'baixados'



}

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


    pastaAtual = fr'{raiz}/{req.tributacao}/Clientes ativos/{req.label}'
    pastaAlvo = fr'{raiz}/{req.tributacaoAlvo}/Clientes ativos/{req.label}'

    print(f'Realizando transformação pasta {pastaAtual} -> {pastaAlvo} ')

    #Limpa arquivos indesejados da pasta
    for nome in ("Thumbs.db", ".DS_Store"):
        for arq in Path(pastaAtual).rglob(nome):
            arq.unlink(missing_ok=True)


    shutil.move(Path(pastaAtual), Path(pastaAlvo))
    acls(pastaAlvo)
    dif = difPastas(fr'src/PastasExemplo/{req.tributacao}/Fiscal',
                    fr'src/PastasExemplo/{req.tributacaoAlvo}/Fiscal')


    add = dif['add']
    rmv = dif['rmv']


    for m in meses:

        if int(m) < int(req.mes): continue

        for a in add:
            try:
                os.makedirs(Path(f'{pastaAlvo}/Fiscal/Ano {ano}/{m}/{a}'))
                print(f'Adicionando /{m}/{a}')

            except FileExistsError:
                continue

        print ('\n')
        for r in rmv:
            try:
                os.removedirs(Path(f'{pastaAlvo}/Fiscal/Ano {ano}/{m}/{r}'))
                print(f'Removendo /{m}/{r}')

            except FileNotFoundError:
                continue

            except OSError:
                continue

    # Contábil (não itera meses)

    print('\nContábil\n')

    dif = difPastas(fr'src/PastasExemplo/{req.tributacao}/Contábil',
                    fr'src/PastasExemplo/{req.tributacaoAlvo}/Contábil')

    add = dif['add']
    rmv = dif['rmv']

    for a in add:
        try:
            os.makedirs(Path(f'{pastaAlvo}/Contábil/Ano {ano}/{a}'))
            print(f'Adicionando /{a}')

        except FileExistsError:
            continue

    print('\n')
    for r in rmv:
        try:
            shutil.rmtree(Path(f'{pastaAlvo}/Contábil/Ano {ano}/{r}'))
            print(f'Removendo /{r}')

        except FileNotFoundError:
            continue

        except OSError:
            continue


def mover(req:MoverRequest, reverse = False):

    pastaOP = pastas[req.op]

    if reverse:
         pastaAlvo = fr'{raiz}/{req.tributacao}/Clientes ativos/{req.label}'
         pastaAtual = fr'{raiz}/{req.tributacao}/Clientes {pastaOP}/{req.label}'

    else:
        pastaAlvo = fr'{raiz}/{req.tributacao}/Clientes {pastaOP}/{req.label}'
        pastaAtual =  fr'{raiz}/{req.tributacao}/Clientes ativos/{req.label}'


    shutil.move(Path(pastaAtual),
                Path(pastaAlvo))

    acls(pastaAlvo)

    return