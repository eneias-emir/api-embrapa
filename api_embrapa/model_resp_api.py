from typing import Optional
from pydantic import BaseModel

class ItensRespApi(BaseModel):
    ano: int
    qtde: int
    valor: Optional[float] | None = None

class RespApi(BaseModel):
    atividade: str
    tipo: Optional[str] = None
    grupo: str
    codigo: str
    produto: str
    itens: list[ItensRespApi] = []

class RespApiImportacaoExportacao(BaseModel):
    atividade: str
    tipo: str
    pais: str
    itens: list[ItensRespApi] = []

