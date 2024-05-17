from sqlalchemy.orm import Mapped, mapped_column

from webapp.database_config import Base


class Producao(Base):
    __tablename__ = 'producao'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True,index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True,index=True)
    categoria: Mapped[str] = mapped_column(primary_key=True,index=True, nullable=True)
    control: Mapped[str] = mapped_column()
    produto: Mapped[str] = mapped_column()


class Comercializacao(Base):
    __tablename__ = 'comercializacao'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True,index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True,index=True)
    categoria: Mapped[str] = mapped_column(primary_key=True,index=True, nullable=True)
    control: Mapped[str] = mapped_column(nullable=True)
    produto: Mapped[str] = mapped_column()


class Processamento(Base):
    __tablename__ = 'processamento'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True,index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True,index=True)
    cultivar: Mapped[str] = mapped_column(primary_key=True,index=True, nullable=True)
    control: Mapped[str] = mapped_column(primary_key=True)
    categoria: Mapped[str] = mapped_column(primary_key=True,index=True, nullable=True)


class Importacao(Base):
    __tablename__ = 'importacao'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True,index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True,index=True, nullable=True)
    categoria: Mapped[str] = mapped_column(primary_key=True,index=True, nullable=True)
    pais: Mapped[str] = mapped_column(primary_key=True,index=True, nullable=True)


class Exportacao(Base):
    __tablename__ = 'exportacao'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True,index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True,index=True,nullable=True)
    categoria: Mapped[str] = mapped_column(primary_key=True,index=True, nullable=True)
    pais: Mapped[str] = mapped_column(primary_key=True,index=True, nullable=True)
