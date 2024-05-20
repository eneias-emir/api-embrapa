from sqlalchemy import create_engine, Integer, String, Float, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker, relationship

from api_embrapa.utils import get_database_file_name

# Criação do mecanismo de banco de dados SQLite
db_file_name = get_database_file_name()
engine = create_engine(f'sqlite:///{db_file_name}', echo=True)

# Base declarativa para as classes ORM
# Base = declarative_base()
class Base(DeclarativeBase):
    pass

# Criação de uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Definição da tabela login
class Login(Base):
    __tablename__ = 'login'
    
    id       = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(100), nullable=False)
    password = mapped_column(String(100), nullable=False)
    

# Definição da tabela dados_embrapa
class DadosEmbrapa(Base):
    __tablename__ = 'dados_embrapa'
    
    id          = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_origem   = mapped_column(Integer, nullable=False)
    opt         = mapped_column(String(10), nullable=False)
    desc_opt    = mapped_column(String(100), nullable=True)
    subopt      = mapped_column(String(10), nullable=True)
    desc_subopt = mapped_column(String(100), nullable=True)
    grupo       = mapped_column(String(50), nullable=True)
    codigo      = mapped_column(String(50), nullable=True)
    descricao   = mapped_column(String(10), nullable=True)
    
    # Relacionamento com a tabela dados_embrapa_itens
    itens = relationship('DadosEmbrapaItens', back_populates='dados_embrapa')

# Definição da tabela dados_embrapa_itens
class DadosEmbrapaItens(Base):
    __tablename__ = 'dados_embrapa_itens'
    
    id               = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_dados_embrapa = mapped_column(Integer, ForeignKey('dados_embrapa.id'), nullable=False)
    opt              = mapped_column(String(10), nullable=False)
    ano              = mapped_column(Integer, nullable=False)
    qtde             = mapped_column(Float, nullable=True)
    valor            = mapped_column(Float, nullable=True)
    
    # Relacionamento com a tabela DADOS
    dados_embrapa = relationship('DadosEmbrapa', back_populates='itens')

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)


