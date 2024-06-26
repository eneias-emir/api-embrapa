from typing import Optional, List
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
    itens: List[ItensRespApi] = []


class RespApiImportacaoExportacao(BaseModel):
    atividade: str
    tipo: str
    pais: str
    itens: List[ItensRespApi] = []


class ApiDescription(BaseModel):
    name: str
    description: str
    endpoints: List[str]


class ItemCsvList(BaseModel):
    opt: str
    subopt: str
    desc_opt: str
    desc_subopt: str
    url: str
