from typing import List, Any, Sequence

from fastapi import APIRouter
from fastapi import Depends
from fastapi.params import Query
from sqlalchemy import Row, RowMapping
from sqlalchemy.orm import Session

from webapp.database_config import get_db
from webapp.models import Producao
from webapp.schemas import ProducaoSchema
from fastapi_sa_orm_filter.operators import Operators as ops
from fastapi_sa_orm_filter.main import FilterCore

# Define fields and operators for filter
my_objects_filter = {
    'ano': [ops.like,ops.contains],
    'qtd': [ops.eq,ops.startswith],
    'categoria': [ops.like,ops.contains],
    'control': [ops.like,ops.contains],
    'produto': [ops.like,ops.contains]
}


router = APIRouter(prefix='/api/producao')


@router.get('', response_model=List[ProducaoSchema])
async def get_filtered_vacancies(
        q: str = Query(default=''),
        db: Session = Depends(get_db)
) -> Sequence[Row[Any] | RowMapping | Any]:
    print(q)
    filter_inst = FilterCore(Producao, my_objects_filter)
    query = filter_inst.get_query(q)

    return  db.execute(query).scalars().all()

# @router.post('', response_model=ProducaoSchema, status_code=status.HTTP_201_CREATED)
# def insert(request: ProducaoSchema):
#     return ProducaoRepository.save(Producao(**request.dict()))


# def update(id: int, request: ProducaoSchema):
#     item = ProducaoRepository.find_by_id(id)
#     if not item:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
#     return ProducaoRepository.save(Producao(**request.dict()))




# @router.get("/{id}")
# def find_by_id(id: int):
#     return ProducaoRepository.find_by_id(id)
#

# @router.delete("/{id}")
# def delete_by_id(id: int):
#     return ProducaoRepository.delete_by_id(id)
#
