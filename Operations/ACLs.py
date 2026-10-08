import subprocess
import os
from Objetos import configs, Path,querryToDF



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
                    set_acl(f"{caminho}/{subF}", grupo, configs['permissoes'][grupo])
                except Exception as e:
                    print(f'Erro ao impor ACLs:\n {e}')
    else:
        print('Sistema Windows, ignorando os ACLs')


def defaultACLs():

    prestadoresCfolders = listaEmpPrestadores()

    raizes = ['Simples Nacional', 'Lucro Real', 'Lucro Presumido']

    for tribut in raizes:
        for cliente in os.listdir(Path(f"/export/Ethos/SERVIDOR/{tribut}/Clientes ativos")):

            print(cliente)
            cod = cliente.split(' - ')[-1]

            for sub in os.listdir(Path(f"/export/Ethos/SERVIDOR/{tribut}/Clientes ativos").joinpath(cliente)):

                try:


                    # Funcionários
                    set_acl(Path(f"/export/Ethos/SERVIDOR/{tribut}/Clientes ativos/{cliente}").joinpath(sub),'funcionarios','rwx')

                    if cod in prestadoresCfolders:
                        print('PrestadoresC !!!')
                        set_acl(Path(f"/export/Ethos/SERVIDOR/{tribut}/Clientes ativos/{cliente}").joinpath(sub),
                                'PrestadoresC', 'rwx')


                except Exception as e:
                    print(cliente, e)


def listaEmpPrestadores():

    """Lista as empresas que os prestadores tem acesso"""

    df = querryToDF("""select ue.i_empresa from bethadba.usConfEmpresas ue where ue.i_confusuario in (2) and ue.modulos != ''""")

    return df['i_empresa'].astype('str').to_list()



if __name__ == "__main__":

    defaultACLs()
