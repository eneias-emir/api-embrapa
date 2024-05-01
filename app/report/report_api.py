from typing import Optional, List

from fastapi import Depends, HTTPException
from fastapi import Query, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app.database_config import get_db
from app.models.report import Report
from app.report.repository import ReportRepository
from app.report.shema import ReportSchema
from app.report.scraping_embrapa_service import get_csv_url_list

router = APIRouter(prefix='/api/report')


@router.get('', response_model=List[ReportSchema])
def find_all(
        db: Session = Depends(get_db),
        type_like: Optional[str] = Query(None),
) -> List[ReportSchema]:
    query = db.query(Report)
    if type_like:
        items = query.filter(Report.type.contains(type_like)).all()
    else:
        items = db.query(Report).all()
    return items


@router.post('', response_model=ReportSchema, status_code=status.HTTP_201_CREATED)
def insert(request: ReportSchema, db: Session = Depends(get_db)):
    return ReportRepository.save(db, Report(**request.dict()))


@router.get("/sincronizar", )
def read_lista_urls_csv(db: Session = Depends(get_db)):
    return get_csv_url_list(db)


@router.put("/{id}", response_model=ReportSchema, status_code=status.HTTP_201_CREATED)
def update(id: int, request: ReportSchema, db: Session = Depends(get_db)):
    item = ReportRepository.find_by_id(db, id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return ReportRepository.save(db, Report(**request.dict()))


@router.get("/{id}")
async def find_by_id(id: int, db: Session = Depends(get_db)):
    return ReportRepository.find_by_id(db, id)


@router.delete("/{id}")
async def delete_by_id(id: int, db: Session = Depends(get_db)):
    return ReportRepository.delete_by_id(db, id)
