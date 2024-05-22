from typing import Type

from sqlalchemy.orm import Session

from app.models.report_item import ReportItem


class ReportItemRepository:
    @staticmethod
    def find_all(db: Session) -> list[Type[ReportItem]]:
        return db.query(ReportItem).all()

    @staticmethod
    def save(db: Session, report_item: ReportItem) -> ReportItem:
        if report_item.id:
            db.merge(report_item)
        else:
            db.add(report_item)
        db.commit()
        return report_item

    @staticmethod
    def find_by_id(db: Session, id: int) -> Type[ReportItem] | None:
        return db.query(ReportItem).filter(ReportItem.id == id).first()

    @staticmethod
    def find_by_report_id(db: Session, report_id: int) -> Type[ReportItem] | None:
        return db.query(ReportItem).filter(ReportItem.report_id == report_id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(ReportItem).filter(ReportItem.id == id).first() is not None

    @staticmethod
    def exists_by_type(db: Session, type: str) -> bool:
        return db.query(ReportItem).filter(ReportItem.type.contains(type)).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        report_item = db.query(ReportItem).filter(ReportItem.id == id).first()
        if report_item is not None:
            db.delete(report_item)
            db.commit()
