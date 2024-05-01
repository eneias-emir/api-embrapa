from typing import List

from pydantic import BaseModel

from app.report_item.shema import ReportItemSchema


class ReportSchema(BaseModel):
    id: int = None
    type: str
    report_items: List[ReportItemSchema]

    class Config:
        orm_mode = True
