from pydantic import BaseModel


class npRequest (BaseModel):

    nome: str
    tributacao: str
    contabilidadeA: bool


"""
'op': 'transformar',
                'label': self.label,
                'tributacaoAtual': self.tributacao,
                'tributacaoAlvo': self.tributacaoAlvo,
                'mes': self.TBtrb_mes.currentText()

"""
class TransformRequest(BaseModel):


    op: str
    label: str
    tributacao: str
    tributacaoAlvo: str
    mes: str

