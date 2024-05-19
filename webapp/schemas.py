from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class AgroindustriaBase(BaseModel):
    """
    Base para esquemas de dados relacionados à agroindústria.

    Args:
        id (int, optional): O ID do item (padrão: None).
        ano (str, optional): O ano do item (padrão: None).
        categoria (str, optional): A categoria do item (padrão: None).
        qtd (int, optional): A quantidade do item (padrão: 0).
    """
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None)
    ano: Optional[str] = Field(default=None)
    categoria: Optional[str] = Field(default=None)
    qtd: Optional[int] = Field(default=0)


class ImportacaoSchema(AgroindustriaBase):
    """
    Esquema para dados de importação na agroindústria.

    Args:
        pais (str, optional): O país de origem (padrão: None).
    """
    pais: Optional[str] = Field(default=None)


class ExportacaoSchema(AgroindustriaBase):
    """
    Esquema para dados de exportação na agroindústria.

    Args:
        pais (str, optional): O país de destino (padrão: None).
    """
    pais: Optional[str] = Field(default=None)


class ProducaoSchema(AgroindustriaBase):
    """
    Esquema para dados de produção na agroindústria.

    Args:
        control (str, optional): O controle do produto (padrão: None).
        produto (str, optional): O produto produzido (padrão: None).
    """
    control: Optional[str] = Field(default=None)
    produto: Optional[str] = Field(default=None)


class ComercializacaoSchema(AgroindustriaBase):
    """
    Esquema para dados de comercialização na agroindústria.

    Args:
        control (str, optional): O controle do produto (padrão: None).
        produto (str, optional): O produto comercializado (padrão: None).
    """
    control: Optional[str] = Field(default=None)
    produto: Optional[str] = Field(default=None)


class ProcessamentoSchema(AgroindustriaBase):
    """
    Esquema para dados de processamento na agroindústria.

    Args:
        control (str, optional): O controle do produto (padrão: None).
        cultivar (str, optional): A cultivar do produto (padrão: None).
    """
    control: Optional[str] = Field(default=None)
    cultivar: Optional[str] = Field(default=None)


class Config:
    """
    Configuração padrão para os modelos Pydantic.
    """
    orm_mode = True
