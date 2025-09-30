from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from fastapi import Depends
from src.database import get_db
from src.models import ImageFrame
from src.repositories.base_repository import BaseRepository


class ImageFrameRepository(BaseRepository[ImageFrame]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(db, ImageFrame)

    def get_by_depth(self, image_id: int, depth: float) -> Optional[ImageFrame]:
        return self.db.query(self.model).filter(
            self.model.image_id == image_id,
            self.model.depth == depth
        ).first()

    def get_frames_with_filters(
        self,
        image_id: int,
        depth_min: Optional[float] = None,
        depth_max: Optional[float] = None,
        skip: int = 0,
        limit: int = 100,
        coloredmap: Optional[bool] = None
    ) -> Tuple[List[ImageFrame], int]:
        if coloredmap is True:
            query = self.db.query(
                self.model.id,
                self.model.image_id,
                self.model.depth,
                self.model.color_map_pixels,
                self.model.colormap_name,
                self.model.created_at,
                self.model.colormap_applied_at
            )
        else:
            query = self.db.query(
                self.model.id,
                self.model.image_id,
                self.model.depth,
                self.model.pixels,
                self.model.colormap_name,
                self.model.created_at,
                self.model.colormap_applied_at
            )

        query = query.filter(self.model.image_id == image_id)

        if depth_min is not None:
            query = query.filter(self.model.depth >= depth_min)
        if depth_max is not None:
            query = query.filter(self.model.depth <= depth_max)

        total = query.count()
        frames = query.order_by(self.model.depth).offset(skip).limit(limit).all()

        return frames, total

    def get_frames_batch(
        self,
        image_id: int,
        offset: int,
        limit: int,
        include_pixels: bool = True
    ) -> List[ImageFrame]:
        if include_pixels:
            query = self.db.query(
                self.model.id,
                self.model.pixels
            ).filter(
                self.model.image_id == image_id,
                self.model.pixels.isnot(None)
            )
        else:
            query = self.db.query(self.model).filter(
                self.model.image_id == image_id
            )

        return query.order_by(self.model.id).offset(offset).limit(limit).all()

    def update_colormap_batch(
        self,
        frame_updates: List[dict],
        colormap_name: str,
        timestamp: datetime
    ) -> None:
        updates = []
        for update in frame_updates:
            updates.append({
                'id': update['id'],
                'color_map_pixels': update['color_map_pixels'],
                'colormap_name': colormap_name,
                'colormap_applied_at': timestamp
            })

        if updates:
            self.bulk_update(updates)

    def count_frames_by_image(self, image_id: int) -> int:
        return self.db.query(func.count(self.model.id)).filter(
            self.model.image_id == image_id
        ).scalar()

    def delete_by_image(self, image_id: int) -> int:
        count = self.db.query(self.model).filter(
            self.model.image_id == image_id
        ).delete()
        self.db.commit()
        return count

    def create_frame(self, image_id: int, depth: float, pixels: list) -> ImageFrame:
        return self.create(
            image_id=image_id,
            depth=depth,
            pixels=pixels
        )

    def bulk_insert(self, mappings: List[dict]) -> None:
        self.db.bulk_insert_mappings(ImageFrame, mappings)
        self.db.commit()