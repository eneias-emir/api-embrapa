from typing import Optional, List, TypeVar, Generic

from pydantic import BaseModel, Field, ConfigDict

# Definindo um tipo genérico para os itens
T = TypeVar('T')


class Page(Generic[T], BaseModel):
    total_items: int
    total_items_page: int
    current_page: int
    total_pages: int
    items: List[T]

    class Config:
        arbitrary_types_allowed = True


class AgroindustriaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None)
    ano: Optional[str] = Field(default=None)
    categoria: Optional[str] = Field(default=None)
    qtd: Optional[int] = Field(default=0)


class ImportacaoSchema(AgroindustriaBase):
    pais: Optional[str] = Field(default=None)


class ExportacaoSchema(AgroindustriaBase):
    pais: Optional[str] = Field(default=None)


class ProducaoSchema(AgroindustriaBase):
    control: Optional[str] = Field(default=None)
    produto: Optional[str] = Field(default=None)


class ComercializacaoSchema(AgroindustriaBase):
    control: Optional[str] = Field(default=None)
    produto: Optional[str] = Field(default=None)


class ProcessamentoSchema(AgroindustriaBase):
    control: Optional[str] = Field(default=None)
    cultivar: Optional[str] = Field(default=None)


class Config:
    orm_mode = True
