import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
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
        try:
            image = self.image_repository.create_image(
                target_width=target_width,
                csv_source=csv_path
            )
            image_id = image.id
            logger.info(f"Created new image record with ID: {image_id}")

            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} rows from CSV")

            frames_processed = 0
            batch_data = []
            batch_size = 1000

            for _, row in df.iterrows():
                frame_data = self.parse_and_resize_row(row, target_width)
                if frame_data:
                    batch_data.append(ImageFrame(
                        image_id=image_id,
                        **frame_data
                    ))
                    frames_processed += 1

                    if len(batch_data) >= batch_size:
                        self.frame_repository.create_many(batch_data)
                        batch_data = []
                        logger.info(f"Processed batch: {frames_processed} frames")

            if batch_data:
                self.frame_repository.create_many(batch_data)

            self.image_repository.update_frame_count(image_id, frames_processed)

            logger.info(f"Successfully processed and saved {frames_processed} frames for image {image_id}")
            return image_id, frames_processed

        except Exception as e:
            logger.error(f"Error in load_resize_and_save: {e}")
            self.frame_repository.rollback()
            raise

    def parse_and_resize_row(self, row: pd.Series, target_width: int) -> Dict:
        try:
            depth = float(row.iloc[0])

            if pd.isna(depth) or np.isinf(depth):
                logger.warning(f"Invalid depth value: {depth}")
                return None

            original_pixels = row.iloc[1:201].values

            if pd.isna(original_pixels).any():
                logger.warning(f"NaN pixel values detected for depth {depth}")
                return None

            original_pixels = original_pixels.astype(int).tolist()

            if len(original_pixels) != 200:
                logger.warning(f"Row has {len(original_pixels)} pixels, expected 200")
                return None

            if not self.image_processor.validate_pixel_values(original_pixels):
                logger.warning(f"Invalid pixel values detected for depth {depth}")
                return None

            resized_pixels = self.image_processor.resize_image_row(original_pixels, target_width)

            return {
                'depth': depth,
                'pixels': resized_pixels
            }

        except Exception as e:
            logger.error(f"Error parsing row: {e}")
            return None