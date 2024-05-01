from typing import Any

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database_config import Base


class Producao(Base):
    __tablename__ = 'producao'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    produto: Mapped[str] = mapped_column(index=True)
    report_item_id: Mapped[int] = mapped_column(ForeignKey("report_item.id"))

    def __init__(self, /, **data: Any):
        super().__init__(**data)

    __table_args__ = (
        *[Column(f"qtd_{str(year)}_em_l", Integer, index=True) for year in range(1970, 2023)],
    )
