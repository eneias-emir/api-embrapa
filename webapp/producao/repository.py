from typing import Type

from sqlalchemy.orm import Session

from webapp.models import Producao


class ProducaoRepository:
    @staticmethod
    def find_all(db: Session) -> list[Type[Producao]]:
        return db.query(Producao).all()

    @staticmethod
    def save(db: Session, producao: Producao) -> Producao:
        if producao.id:
            db.merge(producao)
        else:
            db.add(producao)
        db.commit()
        return producao

    @staticmethod
    def find_by_id(db: Session, id: int) -> Type[Producao] | None:
        return db.query(Producao).filter(Producao.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Producao).filter(Producao.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        producao = db.query(Producao).filter(Producao.id == id).first()
        if producao is not None:
            db.delete(producao)
            db.commit()
