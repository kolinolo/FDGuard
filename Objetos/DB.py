import pandas as pd
import os

import sqlanydb



pwd = os.getenv('PWDSQLANYWHERE')
uid = os.getenv('USERSQLANYWHERE')
host = f'{os.getenv('SERVIDOR')}:{os.getenv('PORTASQLANYWHERE')}'


def conect():

    conexao = sqlanydb.connect(uid=uid,
                               pwd=pwd,
                               host=host,
                               AutoStop="Yes",
                               charset='latin1')
    return  conexao



def querryToDF(comando:str) -> pd.DataFrame:



    conexao = conect()

    cursor = conexao.cursor()
    cursor.execute(comando)
    df = pd.read_sql(comando, conexao)
    cursor.close()
    conexao.close()
    del conexao

    return df
