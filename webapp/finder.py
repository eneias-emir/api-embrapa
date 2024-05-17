from fastapi import Query
from fastapi_sa_orm_filter.main import FilterCore
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import Type, Callable, TypeVar, List, Generic, Any

from webapp.schemas import Page

T = TypeVar('T', bound=BaseModel)


class GenericFinder(Generic[T]):
    def __init__(self, db: Session, model: Type[T], schema: Type[T]):
        self.db = db
        self.model = model
        self.schema = schema

    def find_all(self, q: str = Query(default=''), page: int = Query(default=1, ge=1),
                 limit: int = Query(default=10, le=100), filter_confg:dict = {}) -> Page[T]:
        filter_inst = FilterCore(self.model, filter_confg)
        query = filter_inst.get_query(q)

        total_items = self.db.execute(select(func.count()).select_from(self.model)).scalar()

        # Calculating offset
        offset = (page - 1) * limit

        # Fetching data with pagination
        rows = self.db.execute(query.limit(limit).offset(offset)).scalars().all()

        # Convertendo os objetos ORM para o esquema Pydantic
        items = [self.schema.from_orm(row) for row in rows]

        # Total items in current page
        total_items_page = len(rows)

        return Page[T](
            items=items,
            total_items=total_items,
            total_items_page=total_items_page,
            total_pages=-(-total_items // limit),
            current_page=page
        )
