from typing import List

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database_config import Base
from .producao import Producao


class ReportItem(Base):
    __tablename__ = 'report_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String, index=True)
    url: Mapped[str] = mapped_column(String)
    producoes: Mapped[List["Producao"]] = relationship()
    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"))
