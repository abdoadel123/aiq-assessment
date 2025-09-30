from typing import Tuple, List, Optional
import logging
from fastapi import Depends, HTTPException
from src.repositories import ImageFrameRepository, ImageRepository
from src.models import ImageFrame, Image

logger = logging.getLogger(__name__)


class FrameService:

    def __init__(
        self,
        frame_repository: ImageFrameRepository = Depends(),
        image_repository: ImageRepository = Depends()
    ):
        self.frame_repository = frame_repository
        self.image_repository = image_repository

    def get_image(self, image_id: int) -> Image:
        image = self.image_repository.get_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail=f"Image {image_id} not found")
        return image

    def get_frames_with_filters(
        self,
        image_id: int,
        depth_min: Optional[float] = None,
        depth_max: Optional[float] = None,
        page: int = 1,
        per_page: int = 100,
        coloredmap: Optional[bool] = None
    ) -> Tuple[List[ImageFrame], int, int]:
        self.get_image(image_id)

        offset = (page - 1) * per_page

        frames, total = self.frame_repository.get_frames_with_filters(
            image_id=image_id,
            depth_min=depth_min,
            depth_max=depth_max,
            skip=offset,
            limit=per_page,
            coloredmap=coloredmap
        )

        total_pages = (total + per_page - 1) // per_page if total > 0 else 0

        logger.info(f"Retrieved {len(frames)} frames for image {image_id} (total: {total}, page: {page}/{total_pages})")

        return frames, total, total_pages