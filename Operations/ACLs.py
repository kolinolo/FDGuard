import subprocess
import os
from Objetos import configs, Path



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