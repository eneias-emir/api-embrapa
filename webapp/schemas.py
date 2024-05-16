from typing import Optional

from pydantic.config import ConfigDict
from pydantic.fields import Field
from pydantic.main import BaseModel


class ProducaoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(default=None)
    ano: str = Field(default=None)
    qtd: int = Field(default=None)
    categoria: Optional[str] = Field(default=None)
    control: str = Field(default=None)
    produto: str = Field(default=None)


class Config:
    orm_mode = True
