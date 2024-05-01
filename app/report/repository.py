from typing import Type

from sqlalchemy.orm import Session

from app.models.report import Report


class ReportRepository:
    @staticmethod
    def find_all(db: Session) -> list[Type[Report]]:
        return db.query(Report).all()

    @staticmethod
    def save(db: Session, report: Report) -> Report:
        if report.id:
            db.merge(report)
        else:
            db.add(report)
        db.commit()
        return report

    @staticmethod
    def find_by_id(db: Session, id: int) -> Type[Report] | None:
        return db.query(Report).filter(Report.id == id).first()

    @staticmethod
    def find_by_type(db: Session, type: str) ->  Type[Report] | None:
        return db.query(Report).filter(Report.type.contains(type)).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Report).filter(Report.id == id).first() is not None

    @staticmethod
    def exists_by_type(db: Session, type: str) -> bool:
        return db.query(Report).filter(Report.type == type).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        report = db.query(Report).filter(Report.id == id).first()
        if report is not None:
            db.delete(report)
            db.commit()
