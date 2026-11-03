from pydantic import BaseModel


class npRequest (BaseModel):

    nome: str
    tributacao: str
    contabilidadeA: bool

class TransformRequest(BaseModel):


    op: str
    label: str
    tributacao: str
    tributacaoAlvo: str
    mes: str


class RenomeiaRequest(BaseModel):

    op: str
    caminho: str
    old_label: str
    new_label: str


class MoverRequest(BaseModel):
    op: str
    label: str
    tributacao: str