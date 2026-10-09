import subprocess
import os
from Objetos import configs, Path,querryToDF



def set_acl(path, group, permissions):

    # ACL de acesso em toda a árvore
    subprocess.run([
        "setfacl",
        "-R",
        "-m",
        f"g:{group}:{permissions}",
        path
    ], check=True)

    # ACL padrão em todos os diretórios
    subprocess.run([
        "find",
        path,
        "-type", "d",
        "-exec",
        "setfacl",
        "-d",
        "-m",
        f"g:{group}:{permissions}",
        "{}",
        "+"
    ], check=True)

def acls(caminho ):

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


def defaultACLs(rm=False):

    prestadoresCfolders = listaAcessoDominio(2)
    ramon = listaAcessoDominio(103)

    raizes = [ 'Lucro Presumido', 'Simples Nacional','Lucro Real']

    for tribut in raizes:
        for cliente in os.listdir(Path(f"/export/Ethos/SERVIDOR/{tribut}/Clientes ativos")):

            print('\n',cliente)
            cod = cliente.split(' - ')[-1]

            clienteFldr = Path(f"/export/Ethos/SERVIDOR/{tribut}/Clientes ativos").joinpath(cliente)

            set_acl(clienteFldr, 'funcionarios', 'r-x')

            # Prestadores C
            if cod in prestadoresCfolders:
                print('PrestadoresC')
                set_acl(clienteFldr, 'PrestadoresC', 'r-x')
            elif rm:
                set_acl(clienteFldr, 'PrestadoresC', '---')

            # yasF
            if tribut == 'Lucro Presumido':

                print('YasF')
                set_acl(clienteFldr, 'lucroPresumido', 'r-x')
            elif rm:

                set_acl(clienteFldr, 'lucroPresumido', '---')

            # ramon
            if cod in ramon:

                print('Ramon')
                set_acl(clienteFldr, 'FranciscoRamon', 'r-x')
            elif rm:

                set_acl(clienteFldr, 'FranciscoRamon', '---')



            for sub in os.listdir(clienteFldr):

                subFdr = Path(f"/export/Ethos/SERVIDOR/{tribut}/Clientes ativos/{cliente}").joinpath(sub)
                try:


                    # Funcionários
                    set_acl(subFdr,'funcionarios','rwx')

                    # Prestadores C
                    if cod in prestadoresCfolders:

                        set_acl(subFdr,'PrestadoresC', 'rwx')


                    # Yasmin fermino
                    if tribut == 'Lucro Presumido':
                        set_acl(subFdr,'lucroPresumido', 'rwx')
                    elif rm:
                        set_acl(subFdr, 'lucroPresumido', '---')

                    # Ramon
                    if cod in ramon:
                        set_acl(subFdr,'FranciscoRamon', 'rwx')

                    elif rm:
                        set_acl(subFdr, 'FranciscoRamon', '---')

                except Exception as e:

                    print(subFdr, e)


def listaAcessoDominio(idUser:str):

    """Lista as empresas que os prestadores tem acesso"""

    df = querryToDF(f"""select ue.i_empresa from bethadba.usConfEmpresas ue where ue.i_confusuario in ({idUser}) and ue.modulos != ''""")

    return df['i_empresa'].astype('str').to_list()


def setAclWay(path,group):

    """Seta as acls das pastas até a pasta alvo, todas como read only r-x"""

    slices = path.split('/')


    way = Path(configs.raiz)

    for step in slices:

        way = way.joinpath(step)

        # ACL de acesso em toda a árvore
        subprocess.run([
            "setfacl",
            "-m",
            f"g:{group}:r-x",
            way
        ], check=True)


    pass



if __name__ == "__main__":

    defaultACLs()
