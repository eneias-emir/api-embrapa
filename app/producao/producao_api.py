from typing import Optional, List, Any

from fastapi import Depends, HTTPException
from fastapi import Query, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app.database_config import get_db
from app.models.report_item import Producao
from app.producao.repository import ProducaoRepository
from app.producao.shema import ProducaoSchema
from app.producao.importar_csv import import_producao_csv

router = APIRouter(prefix='/api/producao')


@router.get('', response_model=List[ProducaoSchema])
def find_all(db: Session = Depends(get_db)):
    return db.query(Producao).all()


@router.post('', response_model=ProducaoSchema, status_code=status.HTTP_201_CREATED)
def insert(request: ProducaoSchema):
    return ProducaoRepository.save(Producao(**request.dict()))


def update(id: int, request: ProducaoSchema):
    item = ProducaoRepository.find_by_id(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return ProducaoRepository.save(Producao(**request.dict()))


@router.get("/importar-producao")
def importar_producao_csv(db: Session = Depends(get_db)):
    return import_producao_csv(db)


@router.get("/{id}")
def find_by_id(id: int):
    return ProducaoRepository.find_by_id(id)


@router.delete("/{id}")
def delete_by_id(id: int):
    return ProducaoRepository.delete_by_id(id)


@router.get("/lista_urls_csv")
def read_lista_urls_csv():
    return {"teste": "heee"}
