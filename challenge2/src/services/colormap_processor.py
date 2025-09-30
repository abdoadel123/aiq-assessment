import logging
from typing import Dict
from datetime import datetime, timezone
from fastapi import Depends, HTTPException
from src.utils.colormap import ColormapHandler
from src.repositories import ImageFrameRepository, ImageRepository

logger = logging.getLogger(__name__)


class ColorMapProcessor:

    def __init__(
        self,
        frame_repository: ImageFrameRepository = Depends(),
        image_repository: ImageRepository = Depends()
    ):
        self.frame_repository = frame_repository
        self.image_repository = image_repository

    def apply_colormap_to_image(
        self,
        image_id: int,
        colormap_name: str,
        batch_size: int = 100
    ) -> Dict:
        if not ColormapHandler.is_valid_colormap(colormap_name):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid colormap: {colormap_name}. Available: {ColormapHandler.AVAILABLE_COLORMAPS}"
            )

        image = self.image_repository.get_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail=f"Image {image_id} not found")
        total_frames = self.frame_repository.count_frames_by_image(image_id)
        if total_frames == 0:
            raise ValueError(f"No frames found for image {image_id}")

        total_batches = (total_frames + batch_size - 1) // batch_size

        logger.info(
            f"Starting colormap '{colormap_name}' application for image {image_id}: "
            f"{total_frames} frames in {total_batches} batches"
        )

        offset = 0
        batch_num = 0
        processed = 0

        while offset < total_frames:
            batch_num += 1

            frames = self.frame_repository.get_frames_batch(
                image_id, offset, batch_size, include_pixels=True
            )

            logger.info(
                f"Processing batch {batch_num}/{total_batches}: {len(frames)} frames"
            )

            frame_updates = []
            current_timestamp = datetime.now(timezone.utc)

            for frame in frames:
                try:
                    if frame.pixels:
                        rgb_pixels = ColormapHandler.apply_colormap(
                            frame.pixels,
                            colormap_name
                        )

                        frame_updates.append({
                            'id': frame.id,
                            'color_map_pixels': rgb_pixels
                        })

                        processed += 1

                except Exception as e:
                    logger.error(f"Error applying colormap to frame {frame.id}: {e}")

            if frame_updates:
                self.frame_repository.update_colormap_batch(
                    frame_updates, colormap_name, current_timestamp
                )

            logger.info(
                f"Batch {batch_num} committed: {processed}/{total_frames} frames processed"
            )

            offset += batch_size

        logger.info(f"Colormap application completed: {processed} frames processed")

        return {
            'processed': processed,
            'total': total_frames,
            'colormap': colormap_name
        }