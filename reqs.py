from pydantic import BaseModel


class npRequest (BaseModel):

    nome: str
    tributacao: str
    contabilidadeA: bool
