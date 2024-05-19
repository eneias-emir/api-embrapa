from sqlalchemy.orm import Mapped, mapped_column

from webapp.database import Base


class Producao(Base):
    """
    Classe de modelo para dados de produção.
    """
    __tablename__ = 'producao'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True, index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True, index=True)
    control: Mapped[str] = mapped_column()
    produto: Mapped[str] = mapped_column(primary_key=True)


class Comercializacao(Base):
    """
    Classe de modelo para dados de comercialização.
    """
    __tablename__ = 'comercializacao'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True, index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True, index=True)
    categoria: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=True)
    control: Mapped[str] = mapped_column(nullable=True)
    produto: Mapped[str] = mapped_column()


class Processamento(Base):
    """
    Classe de modelo para dados de processamento.
    """
    __tablename__ = 'processamento'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True, index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True, index=True)
    cultivar: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=True)
    control: Mapped[str] = mapped_column(primary_key=True)
    categoria: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=True)


class Importacao(Base):
    """
    Classe de modelo para dados de importação.
    """
    __tablename__ = 'importacao'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True, index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=True)
    categoria: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=True)
    pais: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=True)


class Exportacao(Base):
    """
    Classe de modelo para dados de exportação.
    """
    __tablename__ = 'exportacao'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ano: Mapped[str] = mapped_column(primary_key=True, index=True)
    qtd: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=True)
    categoria: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=True)
    pais: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=True)
