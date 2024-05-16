from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from webapp.database_config import Base


class Producao(Base):
    __tablename__ = 'producao'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(index=True)
    qtd: Mapped[int] = mapped_column(index=True)
    categoria: Mapped[str] = mapped_column(index=True, nullable=True)
    control: Mapped[str] = mapped_column()
    produto: Mapped[str] = mapped_column()

    #
    # __table_args__ = (
    #     *[Column(f"qtd_{str(year)}_em_l", Integer, index=True) for year in range(1970, 2023)],
    # )
