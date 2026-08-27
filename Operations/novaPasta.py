""" Cria uma pasta no servidor conforme os parâmetros do endpoint """
def NovaPasta(req):
    try:

        if req.tributacao == "Lucro Real":

            tributacao = "Lucro Real"

            pastasFiscal = configs['fiscal']['presumidoReal']
            pastasContabil = configs['contabil']['simples']
            pastasPessoal = configs['pessoal']['simples']

        elif req.tributacao == "Lucro Presumido":

            tributacao = "Lucro Presumido"

            pastasFiscal = configs['fiscal']['presumidoReal']
            pastasContabil = configs['contabil']['simples']
            pastasPessoal = configs['pessoal']['simples']

        elif req.tributacao == 'Simples Nacional':

            tributacao = "Simples Nacional"

            pastasFiscal = configs['fiscal']['simples']
            pastasContabil = configs['contabil']['simples']
            pastasPessoal = configs['pessoal']['simples']

        else:
            raise TributError(req.tributacao)

        # _______________________________________________________________

        nivel = configs['raizPastas']
        anoAtual = configs['ano']

        nomeArquivo = req.nome
        contAnterior = req.contabilidadeA

        if Path(f"{nivel}/{tributacao}/Clientes ativos/{nomeArquivo}").exists(): raise pastaExistenteError(nomeArquivo)

        Path(f"{nivel}/{tributacao}/Clientes ativos/{nomeArquivo}").mkdir(parents=True)

        nivel = f"{nivel}/{tributacao}/Clientes ativos/{nomeArquivo}"

        for departamento in configs['departamentos'][:3]:

            for mes in meses:
                Path(f"{nivel}/{departamento}/Ano {anoAtual}/{mes}").mkdir(parents=True)
                f"{nivel}/{departamento}/Ano {anoAtual}/{mes}"

                if departamento == "Fiscal":
                    for pastaFiscal in pastasFiscal:
                        Path(f"{nivel}/{departamento}/Ano {anoAtual}/{mes}/{pastaFiscal}").mkdir(parents=True)


                elif departamento == "Pessoal":
                    for pastaPessoal in pastasPessoal:
                        Path(f"{nivel}/{departamento}/Ano {anoAtual}/{mes}/{pastaPessoal}").mkdir(parents=True)

            if departamento == "Contábil":

                if tributacao == "Simples Nacional":

                    Path(f"{nivel}/{departamento}/Ano {anoAtual}/Livro Contábil Autenticado").mkdir(parents=True)


                else:

                    Path(f"{nivel}/{departamento}/Ano {anoAtual}/Declarações Anuais").mkdir(parents=True)

                Path(f"{nivel}/{departamento}/Ano {anoAtual}/Fechamento Anual").mkdir(parents=True)

                if contAnterior: Path(f"{nivel}/{departamento}/Contabilidade Anterior").mkdir(parents=True)

                if tributacao != "Simples Nacional":
                    Path(f"{nivel}/{departamento}/Ano {anoAtual}/Declarações Anuais/ECD").mkdir(parents=True)
                    Path(f"{nivel}/{departamento}/Ano {anoAtual}/Declarações Anuais/ECF").mkdir(parents=True)


            elif departamento == "Fiscal":
                Path(f"{nivel}/{departamento}/Ano {anoAtual}/Declarações Anuais/DIMOB").mkdir(parents=True)
                Path(f"{nivel}/{departamento}/Ano {anoAtual}/Declarações Anuais/DIMED").mkdir(parents=True)
                if contAnterior: Path(f"{nivel}/{departamento}/Contabilidade Anterior").mkdir(parents=True)

                if tributacao == "Simples Nacional":
                    Path(f"{nivel}/{departamento}/Ano {anoAtual}/Declarações Anuais/DEFIS").mkdir(parents=True)

            elif departamento == "Pessoal":
                Path(f"{nivel}/{departamento}/Ano {anoAtual}/Declarações Anuais/DIRF").mkdir(parents=True)
                Path(f"{nivel}/{departamento}/Ano {anoAtual}/Declarações Anuais/RAIS").mkdir(parents=True)
                if contAnterior: Path(f"{nivel}/{departamento}/Contabilidade Anterior").mkdir(parents=True)

        departamento = 'Societário'
        nivel = f"{configs['raizPastas']}/{tributacao}/Clientes ativos/{nomeArquivo}/Societário"

        Path(f"{nivel}/CND/{anoAtual}").mkdir(parents=True)
        for mes in meses:
            Path(f"{nivel}/CND/{anoAtual}/{mes}").mkdir(parents=True)
            for cnd in configs['cnds']:
                Path(f"{nivel}/CND/{anoAtual}/{mes}/{cnd}").mkdir(parents=True)

        Path(f"{nivel}/Docs Cadastrais").mkdir(parents=True)
        Path(f"{nivel}/Docs Cadastrais/Procuração").mkdir(parents=True)
        Path(f"{nivel}/Docs Cadastrais/Processos/Abertura").mkdir(parents=True)

        for alvara in configs['alvaras']:
            Path(f"{nivel}/Docs Cadastrais/Alvarás/{anoAtual}/{alvara}").mkdir(parents=True)

        for pastaSocietario in ["Cods e Acesso da Empresa", "Docs CNPJ", "Notificações multas", "Docs sócios",
                                "Termos de Responsabilidade"]:
            Path(f"{nivel}/Docs Cadastrais/{pastaSocietario}").mkdir(parents=True)

        Path(f"{configs['raizPastas']}/{tributacao}/Clientes ativos/{nomeArquivo}/Reuniões").mkdir(parents=True)

        # ____

        acls(f"{configs['raizPastas']}/{tributacao}/Clientes ativos/{nomeArquivo}")

        return 200, 'pasta criada com sucesso'

    except pastaExistenteError as e:
        return 401, e