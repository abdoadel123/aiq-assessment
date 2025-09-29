import asyncio
import logging
from typing import Dict
from sqlalchemy import func
from datetime import datetime, timezone
from src.database.models import ImageFrame
from src.utils.colormap import ColormapHandler
from src.database import SessionLocal

logger = logging.getLogger(__name__)


class ColorMapProcessor:

    _instance = None
    _processing_status: Dict = {
        'status': 'idle',
        'processed': 0,
        'total': 0,
        'current_batch': 0,
        'total_batches': 0,
        'colormap': None
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_status(cls) -> Dict:
        return cls._processing_status.copy()

    @classmethod
    async def apply_colormap_batch(cls, colormap_name: str, batch_size: int = 100):
        if cls._processing_status['status'] == 'processing':
            raise ValueError("Colormap processing already in progress")

        cls._processing_status = {
            'status': 'processing',
            'processed': 0,
            'total': 0,
            'current_batch': 0,
            'total_batches': 0,
            'colormap': colormap_name
        }

        db = SessionLocal()
        try:
            total_frames = db.query(func.count(ImageFrame.id)).scalar()
            cls._processing_status['total'] = total_frames
            cls._processing_status['total_batches'] = (total_frames + batch_size - 1) // batch_size

            logger.info(f"Starting colormap '{colormap_name}' application for {total_frames} frames in {cls._processing_status['total_batches']} batches")

            offset = 0
            batch_num = 0

            while offset < total_frames:
                batch_num += 1
                cls._processing_status['current_batch'] = batch_num

                frames = db.query(ImageFrame.id, ImageFrame.pixels).filter(ImageFrame.pixels.isnot(None)).order_by(ImageFrame.id).offset(offset).limit(batch_size).all()

                logger.info(f"Processing batch {batch_num}/{cls._processing_status['total_batches']}: {len(frames)} frames")

                frame_updates = []
                for frame in frames:
                    try:
                        if frame.pixels:
                            rgb_pixels = ColormapHandler.apply_colormap(
                                frame.pixels,
                                colormap_name
                            )

                            frame_updates.append({
                                'id': frame.id,
                                'color_map_pixels': rgb_pixels,
                                'colormap_name': colormap_name,
                                'colormap_applied_at': datetime.now(timezone.utc)
                            })

                            cls._processing_status['processed'] += 1

                    except Exception as e:
                        logger.error(f"Error applying colormap to frame {frame.id}: {e}")

                if frame_updates:
                    db.bulk_update_mappings(ImageFrame, frame_updates)
                db.commit()
                logger.info(f"Batch {batch_num} committed: {cls._processing_status['processed']}/{total_frames} frames processed")

                await asyncio.sleep(0.1)

                offset += batch_size

            cls._processing_status['status'] = 'completed'
            logger.info(f"Colormap application completed: {cls._processing_status['processed']} frames processed")

        except Exception as e:
            logger.error(f"Error in batch colormap processing: {e}")
            cls._processing_status['status'] = 'error'
            db.rollback()
            raise
        finally:
            db.close()

    @classmethod
    def reset_status(cls):
        cls._processing_status = {
            'status': 'idle',
            'processed': 0,
            'total': 0,
            'current_batch': 0,
            'total_batches': 0,
            'colormap': None
        }