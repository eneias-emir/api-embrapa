from typing import Optional, List

from fastapi import Depends, HTTPException
from fastapi import Query, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app.database_config import get_db
from app.models.report_item import ReportItem
from app.report_item.repository import ReportItemRepository
from app.report_item.shema import ReportItemSchema

router = APIRouter(prefix='/api/report-item')


@router.get('',response_model=List[ReportItemSchema])
def find_all(
        db: Session = Depends(get_db),
        type_like: Optional[str] = Query(None),
):
    query = db.query(ReportItem)
    if type_like:
        items = query.filter(ReportItem.type.contains(type_like)).all()
    else:
        items = db.query(ReportItem).all()
    return items


@router.post('', response_model=ReportItemSchema, status_code=status.HTTP_201_CREATED)
def insert(request: ReportItemSchema, db: Session = Depends(get_db)):
    return ReportItemRepository.save(db, ReportItem(**request.dict()))


@router.put("/{id}", response_model=ReportItemSchema, status_code=status.HTTP_201_CREATED)
def update(id: int, request: ReportItemSchema, db: Session = Depends(get_db)):
    item = ReportItemRepository.find_by_id(db, id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return ReportItemRepository.save(db, ReportItem(**request.dict()))


@router.get("/{id}")
def find_by_id(id: int, db: Session = Depends(get_db)):
    return ReportItemRepository.find_by_id(db, id)


@router.delete("/{id}")
def delete_by_id(id: int, db: Session = Depends(get_db)):
    return ReportItemRepository.delete_by_id(db, id)


@router.get("/lista_urls_csv")
def read_lista_urls_csv():
    return {"teste": "heee"}
