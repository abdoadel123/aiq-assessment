import pandas as pd
import numpy as np
from typing import  Dict, Tuple
import logging
from fastapi import Depends
from src.models import ImageFrame
from src.services.image_processor import ImageProcessor
from src.repositories import ImageFrameRepository, ImageRepository

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(
        self,
        frame_repository: ImageFrameRepository = Depends(),
        image_repository: ImageRepository = Depends()
    ):
        self.frame_repository = frame_repository
        self.image_repository = image_repository
        self.image_processor = ImageProcessor()

    def load_resize_and_save(self, csv_path: str, target_width: int = 150) -> Tuple[int, int]:
        image = self.image_repository.create_image(
            target_width=target_width,
            csv_source=csv_path
        )
        image_id = image.id
        logger.info(f"Created new image record with ID: {image_id}")

        frames_processed = 0
        batch_data = []
        batch_size = 5000

        for chunk in pd.read_csv(csv_path, chunksize=10000):
            chunk = chunk.dropna().reset_index(drop=True)
            chunk = chunk[np.isfinite(chunk.iloc[:, 0])]

            for row in chunk.itertuples(index=False):
                frame_data = self.parse_and_resize_row(row, target_width)
                if frame_data:
                    batch_data.append({
                        "image_id": image_id,
                        **frame_data
                    })
                    frames_processed += 1

                    if len(batch_data) >= batch_size:
                        self.frame_repository.bulk_insert(batch_data)
                        batch_data = []
                        logger.info(f"Processed batch: {frames_processed} frames")

        if batch_data:
            self.frame_repository.bulk_insert(batch_data)

        self.image_repository.update_frame_count(image_id, frames_processed)
        logger.info(f"Successfully processed {frames_processed} frames for image {image_id}")

        return image_id, frames_processed

    def parse_and_resize_row(self, row, target_width: int) -> Dict:
        try:
            depth = float(row[0])

            if pd.isna(depth) or np.isinf(depth):
                return None

            original_pixels = np.array(row[1:201], dtype=np.float64)

            if np.isnan(original_pixels).any():
                return None

            if len(original_pixels) != 200:
                return None

            original_pixels = original_pixels.astype(np.int32)

            if not ((original_pixels >= 0) & (original_pixels <= 255)).all():
                return None

            resized_pixels = self.image_processor.resize_image_row(original_pixels.tolist(), target_width)

            return {
                'depth': depth,
                'pixels': resized_pixels
            }

        except Exception as e:
            logger.error(f"Error parsing row: {e}")
            return None