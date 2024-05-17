from fastapi import APIRouter, Depends, Query
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
    'ano': [ops.like, ops.contains, ops.startswith],
    'qtd': [ops.eq, ops.startswith],
    'categoria': [ops.like, ops.contains, ops.startswith],
    'control': [ops.like, ops.contains, ops.startswith],
    'cultivar': [ops.like, ops.contains, ops.startswith],
    'pais': [ops.like, ops.contains, ops.startswith],
    'produto': [ops.like, ops.contains, ops.startswith]
}

q_examples = {
    "Exemplo 1": {
        "summary": "Exemplo de consulta utilizando like, ou seja irá buscar todos que contém do inicio o valor "
                   "definido, funciona para todos os campos exeto qtd",
        "value": "control__like=2023"
    },
    "Exemplo 2": {
        "summary": "Exemplo de consulta utilizando que começa com o valor definido",
        "value": "qtd__startswith=842"
    },
    "Exemplo 3": {
        "summary": "Exemplo de consulta utilizando ele irá buscar todos os registros que contém o valor passado, "
                   "funciona para todos os campos exeto qtd",
        "value": "ano__contains=2023"
    },
    "Exemplo 4": {
        "summary": "Exemplo de consulta utilizando equals ou seja neste caso tem que ser iguaao valor, eq só funciona "
                   "para qtd",
        "value": "qtd__eq=2023"
    }
}

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

    Exemplos de consulta:
        - Filtrar por ano que contém '2023': /api/producao?q=ano_contains=2023
        - Filtrar por quantidade que começa com '100': /api/producao?q=qtd_startswith=100
        - Filtrar por control que contém 'de': /api/producao?q=control_contains=de

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
async def find_all_processamento(
        q: str = Query(default='', example=q_examples),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ProcessamentoSchema]:
    """
    Endpoint para recuperar todos os registros de processamento.

    Exemplos de consulta:
        - Filtrar por categoria que contém 'frutas': /api/processamento?q=categoria_contains=frutas
        - Filtrar por país que contém 'Brasil': /api/processamento?q=pais_contains=Brasil

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
async def find_all_comercializacao(
        q: str = Query(default='', example=q_examples),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ComercializacaoSchema]:
    """
    Endpoint para recuperar todos os registros de comercialização.

    Exemplos de consulta:
        - Filtrar por produto que contém 'soja': /api/comercializacao?q=produto_contains=soja
        - Filtrar por cultivar que contém 'transgênico': /api/comercializacao?q=cultivar_contains=transgênico

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
async def find_all_exportacao(
        q: str = Query(default='', example=q_examples),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ExportacaoSchema]:
    """
    Endpoint para recuperar todos os registros de exportação.

    Exemplos de consulta:
        - Filtrar por ano que contém '2022': /api/exportacao?q=ano_contains=2022
        - Filtrar por quantidade que é igual a '5000': /api/exportacao?q=qtd_eq=5000

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
async def find_all_importacao(
        q: str = Query(default='', example=q_examples),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, le=100),
        db: Session = Depends(get_db)
) -> Page[ImportacaoSchema]:
    """
    Endpoint para recuperar todos os registros de importação.

    Exemplos de consulta:
        - Filtrar por país que contém 'Argentina': /api/importacao?q=pais_contains=Argentina
        - Filtrar por produto que contém 'trigo': /api/importacao?q=produto_contains=trigo

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
