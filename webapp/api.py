from fastapi import APIRouter
from fastapi import Depends
from fastapi.params import Query
from fastapi_sa_orm_filter.operators import Operators as ops
from sqlalchemy.orm import Session

from webapp.database import get_db
from webapp.finder import GenericFinder
from webapp.models import Producao, Processamento, Comercializacao, Exportacao, Importacao
from webapp.schemas import ProducaoSchema, ProcessamentoSchema, ComercializacaoSchema, ExportacaoSchema, \
    ImportacaoSchema
from webapp.utils import Page

# Define fields and operators for filter
my_objects_filter = {
    'ano': [ops.like, ops.contains],
    'qtd': [ops.eq, ops.startswith],
    'categoria': [ops.like, ops.contains],
    'control': [ops.like, ops.contains],
    'cultivar': [ops.like, ops.contains],
    'pais': [ops.like, ops.contains],
    'produto': [ops.like, ops.contains]
}

router = APIRouter()


@router.get('/api/producao', response_model=Page[ProducaoSchema])
async def findAllProducao(
        q: str = Query(default=''),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ProducaoSchema]:
    """
    Endpoint para recuperar todos os registros de produção.

    Args:
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).
        page (int, optional): Número da página para paginar os resultados (padrão: 1).
        limit (int, optional): Limite de itens por página (padrão: 10).
        db (Session): Sessão do banco de dados.

    Returns:
        Page[ProducaoSchema]: Página de resultados paginados de produção.
    """
    finder = GenericFinder(db=db, model=Producao, schema=ProducaoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)


@router.get('/api/processamento', response_model=Page[ProcessamentoSchema])
async def findAllProcessamento(
        q: str = Query(default=''),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ProcessamentoSchema]:
    """
    Endpoint para recuperar todos os registros de processamento.

    Args:
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).
        page (int, optional): Número da página para paginar os resultados (padrão: 1).
        limit (int, optional): Limite de itens por página (padrão: 10).
        db (Session): Sessão do banco de dados.

    Returns:
        Page[ProcessamentoSchema]: Página de resultados paginados de processamento.
    """
    finder = GenericFinder(db=db, model=Processamento, schema=ProcessamentoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)


@router.get('/api/comercializacao', response_model=Page[ComercializacaoSchema])
async def findAllComercializacao(
        q: str = Query(default=''),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ComercializacaoSchema]:
    """
    Endpoint para recuperar todos os registros de comercialização.

    Args:
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).
        page (int, optional): Número da página para paginar os resultados (padrão: 1).
        limit (int, optional): Limite de itens por página (padrão: 10).
        db (Session): Sessão do banco de dados.

    Returns:
        Page[ComercializacaoSchema]: Página de resultados paginados de comercialização.
    """
    finder = GenericFinder(db=db, model=Comercializacao, schema=ComercializacaoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)


@router.get('/api/exportacao', response_model=Page[ExportacaoSchema])
async def findAllExportacao(
        q: str = Query(default=''),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ExportacaoSchema]:
    """
    Endpoint para recuperar todos os registros de exportação.

    Args:
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).
        page (int, optional): Número da página para paginar os resultados (padrão: 1).
        limit (int, optional): Limite de itens por página (padrão: 10).
        db (Session): Sessão do banco de dados.

    Returns:
        Page[ExportacaoSchema]: Página de resultados paginados de exportação.
    """
    finder = GenericFinder(db=db, model=Exportacao, schema=ExportacaoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)


@router.get('/api/importacao', response_model=Page[ImportacaoSchema])
async def findAllImportacao(
        q: str = Query(default=''),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ImportacaoSchema]:
    """
    Endpoint para recuperar todos os registros de importação.

    Args:
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).
        page (int, optional): Número da página para paginar os resultados (padrão: 1).
        limit (int, optional): Limite de itens por página (padrão: 10).
        db (Session): Sessão do banco de dados.

    Returns:
        Page[ImportacaoSchema]: Página de resultados paginados de importação.
    """
    finder = GenericFinder(db=db, model=Importacao, schema=ImportacaoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)
