from fastapi import APIRouter, Depends, Query
from fastapi_sa_orm_filter.operators import Operators as ops
from sqlalchemy.orm import Session

from webapp.database import get_db
from webapp.utils import GenericFinder
from webapp.models import Producao, Processamento, Comercializacao, Exportacao, Importacao
from webapp.schemas import ProducaoSchema, ProcessamentoSchema, ComercializacaoSchema, ExportacaoSchema, \
    ImportacaoSchema
from webapp.utils import Page

# Define fields and operators for filter
my_objects_filter = {
    'ano': [ops.like, ops.contains, ops.startswith],
    'qtd': [ops.eq, ops.startswith],
    'categoria': [ops.like, ops.contains, ops.startswith],
    'control': [ops.like, ops.contains, ops.startswith],
    'cultivar': [ops.like, ops.contains, ops.startswith],
    'pais': [ops.like, ops.contains, ops.startswith],
    'produto': [ops.like, ops.contains, ops.startswith]
}

q_examples = "categoria__like=Sem classificação&qtd__eq=152517&ano__startswith=2000"


router = APIRouter()


@router.get('/api/producao', response_model=Page[ProducaoSchema])
async def find_all_producao(
        q: str = Query(default='', example=q_examples),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ProducaoSchema]:
    """
    Endpoint para recuperar todos os registros de produção.

    Exemplos de consulta:\n
        - Filtrar por ano que contém '2023': /api/producao?q=ano__contains=2023\n
        - Filtrar por quantidade que começa com '100': /api/producao?q=qtd__startswith=100\n
        - Filtrar por control que contém 'de': /api/producao?q=control__contains=de

    Args:
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).\n
        page (int, optional): Número da página para paginar os resultados (padrão: 1).\n
        limit (int, optional): Limite de itens por página (padrão: 10).\n
        db (Session): Sessão do banco de dados.\n

    Returns:\n
        Page[ProducaoSchema]: Página de resultados paginados de produção.
    """
    finder = GenericFinder(db=db, model=Producao, schema=ProducaoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)


@router.get('/api/processamento', response_model=Page[ProcessamentoSchema])
async def find_all_processamento(
        q: str = Query(default='', example=q_examples),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ProcessamentoSchema]:
    """
    Endpoint para recuperar todos os registros de processamento.

    Exemplos de consulta:\n
        - Filtrar por categoria que contém 'frutas': /api/processamento?q=categoria__contains=frutas\n
        - Filtrar por país que contém 'Brasil': /api/processamento?q=pais__contains=Brasil\n

    Args:\n
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).\n
        page (int, optional): Número da página para paginar os resultados (padrão: 1).\n
        limit (int, optional): Limite de itens por página (padrão: 10).\n
        db (Session): Sessão do banco de dados.\n

    Returns:\n
        Page[ProcessamentoSchema]: Página de resultados paginados de processamento.
    """
    finder = GenericFinder(db=db, model=Processamento, schema=ProcessamentoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)


@router.get('/api/comercializacao', response_model=Page[ComercializacaoSchema])
async def find_all_comercializacao(
        q: str = Query(default='', example=q_examples),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ComercializacaoSchema]:
    """
    Endpoint para recuperar todos os registros de comercialização.

    Exemplos de consulta:\n
        - Filtrar por produto que contém 'soja': /api/comercializacao?q=produto__contains=soja\n
        - Filtrar por cultivar que contém 'transgênico': /api/comercializacao?q=cultivar__contains=transgênico\n

    Args:\n
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).\n
        page (int, optional): Número da página para paginar os resultados (padrão: 1).\n
        limit (int, optional): Limite de itens por página (padrão: 10).\n
        db (Session): Sessão do banco de dados.\n

    Returns:\n
        Page[ComercializacaoSchema]: Página de resultados paginados de comercialização.
    """
    finder = GenericFinder(db=db, model=Comercializacao, schema=ComercializacaoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)


@router.get('/api/exportacao', response_model=Page[ExportacaoSchema])
async def find_all_exportacao(
        q: str = Query(default='', example=q_examples),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ExportacaoSchema]:
    """
    Endpoint para recuperar todos os registros de exportação.

    Exemplos de consulta:\n
        - Filtrar por ano que contém '2022': /api/exportacao?q=ano__contains=2022\n
        - Filtrar por quantidade que é igual a '5000': /api/exportacao?q=qtd_eq=5000\n

    Args:
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).\n
        page (int, optional): Número da página para paginar os resultados (padrão: 1).\n
        limit (int, optional): Limite de itens por página (padrão: 10).\n
        db (Session): Sessão do banco de dados.\n

    Returns:\n
        Page[ExportacaoSchema]: Página de resultados paginados de exportação.
    """
    finder = GenericFinder(db=db, model=Exportacao, schema=ExportacaoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)


@router.get('/api/importacao', response_model=Page[ImportacaoSchema])
async def find_all_importacao(
        q: str = Query(default='', example=q_examples),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ImportacaoSchema]:
    """
    Endpoint para recuperar todos os registros de importação.

    Exemplos de consulta:\n
        - Filtrar por país que contém 'Argentina': /api/importacao?q=pais__contains=Argentina\n
        - Filtrar por produto que contém 'trigo': /api/importacao?q=produto__contains=trigo\n

    Args:\n
        q (str, optional): Consulta opcional para filtrar os resultados (padrão: vazio).\n
        page (int, optional): Número da página para paginar os resultados (padrão: 1).\n
        limit (int, optional): Limite de itens por página (padrão: 10).\n
        db (Session): Sessão do banco de dados.\n

    Returns:\n
        Page[ImportacaoSchema]: Página de resultados paginados de importação.
    """
    finder = GenericFinder(db=db, model=Importacao, schema=ImportacaoSchema)
    return finder.find_all(q=q, page=page, limit=limit, filter_config=my_objects_filter)
