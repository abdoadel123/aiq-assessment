from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

T = TypeVar('T')


class BaseRepository(Generic[T]):

    def __init__(self, db_session: Session, model: Type[T]):
        self.db = db_session
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(func.count(self.model.id)).scalar()

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def create_many(self, items: List[T]) -> None:
        self.db.add_all(items)
        self.db.commit()

    def update(self, id: int, **kwargs) -> Optional[T]:
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    def bulk_update(self, mappings: List[Dict[str, Any]]) -> None:
        self.db.bulk_update_mappings(self.model, mappings)
        self.db.commit()

    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False

    def delete_all(self) -> int:
        count = self.db.query(self.model).delete()
        self.db.commit()
        return count

    def rollback(self) -> None:
        self.db.rollback()