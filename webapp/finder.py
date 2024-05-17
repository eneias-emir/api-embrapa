from typing import Type, TypeVar, Generic, Dict

from fastapi import Query
from fastapi_sa_orm_filter.main import FilterCore
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from webapp.utils import Page

T = TypeVar('T', bound=BaseModel)


class GenericFinder(Generic[T]):
    """
    Classe para buscar registros páginado de um modelo específico no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        model (Type[T]): Modelo SQLAlchemy.
        schema (Type[T]): Esquema Pydantic correspondente ao modelo.

    Attributes:
        db (Session): Sessão do banco de dados.
        model (Type[T]): Modelo SQLAlchemy.
        schema (Type[T]): Esquema Pydantic correspondente ao modelo.
    """
    def __init__(self, db: Session, model: Type[T], schema: Type[T]):
        self.db = db
        self.model = model
        self.schema = schema

    def find_all(self, q: str = Query(default=''), page: int = Query(default=1, ge=1),
                 limit: int = Query(default=10, le=100), filter_config: Dict = {}) -> Page[T]:
        """
        Recupera todos os registros com suporte para paginação e filtragem.

        Args:
            q (str, optional): String de consulta para filtrar os resultados (padrão: vazio).
            page (int, optional): Número da página para paginar os resultados (padrão: 1).
            limit (int, optional): Limite de itens por página (padrão: 10).
            filter_config (Dict, optional): Configuração de filtro para os atributos do modelo (padrão: vazio).

        Returns:
            Page[T]: Página de resultados paginados e filtrados.
        """
        # Inicializa o objeto de filtro
        filter_inst = FilterCore(self.model, filter_config)

        # Obtém a consulta filtrada
        query = filter_inst.get_query(q)

        # Total de itens na base de dados
        total_items = self.db.execute(select(func.count()).select_from(self.model)).scalar()

        # Calcula o deslocamento para a paginação
        offset = (page - 1) * limit

        # Obtém os dados com paginação
        rows = self.db.execute(query.limit(limit).offset(offset)).scalars().all()

        # Converte os objetos ORM para o esquema Pydantic
        items = [self.schema.from_orm(row) for row in rows]

        # Total de itens na página atual
        total_items_page = len(rows)

        # Calcula o total de páginas
        total_pages = -(-total_items // limit)

        return Page[T](
            items=items,
            total_items=total_items,
            total_items_page=total_items_page,
            total_pages=total_pages,
            current_page=page
        )
