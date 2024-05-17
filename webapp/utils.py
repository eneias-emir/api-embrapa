from typing import List, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')


class Page(BaseModel, Generic[T]):
    """
    Representa uma página de resultados paginados.

    Args:
        total_items (int): O número total de itens.
        total_items_page (int): O número total de itens por página.
        current_page (int): O número da página atual.
        total_pages (int): O número total de páginas.
        items (List[T]): Lista de itens na página.
    """
    total_items: int
    total_items_page: int
    current_page: int
    total_pages: int
    items: List[T]

    class Config:
        arbitrary_types_allowed = True
