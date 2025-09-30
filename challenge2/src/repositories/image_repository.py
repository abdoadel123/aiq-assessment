from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database import get_db
from src.models import Image
from src.repositories.base_repository import BaseRepository


class ImageRepository(BaseRepository[Image]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(db, Image)

    def create_image(self, target_width: int, csv_source: str = None) -> Image:
        return self.create(
            target_width=target_width,
            csv_source=csv_source,
            total_frames=0
        )

    def update_frame_count(self, image_id: int, total_frames: int) -> Optional[Image]:
        return self.update(image_id, total_frames=total_frames)

    def get_by_id(self, image_id: int) -> Optional[Image]:
        return super().get_by_id(image_id)