from typing import List

from pydantic import BaseModel

from app.producao.shema import ProducaoSchema


class ReportItemSchema(BaseModel):
    id: int = None
    type: str
    url: str
    report_id: int
    producoes: List[ProducaoSchema]

    class Config:
        orm_mode = True
