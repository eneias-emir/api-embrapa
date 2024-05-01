from typing import List

from sqlalchemy import Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .report_item import ReportItem
from app.database_config import Base


class Report(Base):
    __tablename__ = "report"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    type: Mapped[str] = mapped_column(index=True)
    report_items: Mapped[List["ReportItem"]] = relationship()

