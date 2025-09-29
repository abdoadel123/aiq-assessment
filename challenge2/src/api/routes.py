from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from src.database import get_db
from src.models import ImageFrame
from src.services.data_loader import DataLoader
from src.services.colormap_processor import ColorMapProcessor
from src.utils.colormap import ColormapHandler
from . import schemas
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["images"])


@router.post("/resize", response_model=schemas.ResizeResponse)
async def resize_images(
    request: schemas.ResizeRequest = Body(...),
    db: Session = Depends(get_db)
):
    try:
        data_loader = DataLoader(db)
        frames_processed = data_loader.load_resize_and_save(
            csv_path="data.csv",
            target_width=request.target_width
        )

        return schemas.ResizeResponse(
            message=f"Successfully processed and resized {frames_processed} frames",
            frames_processed=frames_processed,
            target_width=request.target_width
        )
    except Exception as e:
        logger.error(f"Error in resize endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/frames", response_model=schemas.FramesQueryResponse)
async def get_frames(
    depth_min: Optional[float] = Query(None, description="Minimum depth value"),
    depth_max: Optional[float] = Query(None, description="Maximum depth value"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page (max 1000)"),
    coloredmap: Optional[bool] = Query(None, description="Return colormap pixels (true) or grayscale pixels (false)"),
    db: Session = Depends(get_db)
):
    try:
        if coloredmap is True:
            query = db.query(
                ImageFrame.id,
                ImageFrame.depth,
                ImageFrame.color_map_pixels,
                ImageFrame.colormap_name,
                ImageFrame.created_at,
                ImageFrame.colormap_applied_at
            )
        else:
            query = db.query(
                ImageFrame.id,
                ImageFrame.depth,
                ImageFrame.pixels,
                ImageFrame.colormap_name,
                ImageFrame.created_at,
                ImageFrame.colormap_applied_at
            )

        if depth_min is not None:
            query = query.filter(ImageFrame.depth >= depth_min)
        if depth_max is not None:
            query = query.filter(ImageFrame.depth <= depth_max)

        total = query.count()
        logger.info(f"Found {total} frames matching filters: depth_min={depth_min}, depth_max={depth_max}, coloredmap={coloredmap}")

        if total == 0:
            return schemas.FramesQueryResponse(
                frames=[],
                count=0,
                total=0,
                page=page,
                per_page=per_page,
                total_pages=0
            )

        total_pages = (total + per_page - 1) // per_page
        offset = (page - 1) * per_page

        frames = query.order_by(ImageFrame.depth).offset(offset).limit(per_page).all()
        logger.info(f"Retrieved {len(frames)} frames for page {page}")

        frame_responses = []
        if coloredmap is True:
            frame_responses = [
                schemas.FrameResponse(
                    id=frame.id,
                    depth=frame.depth,
                    pixels=[],
                    color_map_pixels=frame.color_map_pixels if frame.color_map_pixels is not None else [],
                    colormap_name=frame.colormap_name,
                    created_at=frame.created_at,
                    colormap_applied_at=frame.colormap_applied_at
                ) for frame in frames
            ]
        else:
            frame_responses = [
                schemas.FrameResponse(
                    id=frame.id,
                    depth=frame.depth,
                    pixels=frame.pixels if frame.pixels is not None else [],
                    color_map_pixels=[],
                    colormap_name=frame.colormap_name,
                    created_at=frame.created_at,
                    colormap_applied_at=frame.colormap_applied_at
                ) for frame in frames
            ]

        return schemas.FramesQueryResponse(
            frames=frame_responses,
            count=len(frame_responses),
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
    except Exception as e:
        logger.error(f"Error in get_frames endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/colormap/apply", response_model=schemas.ColorMapResponse)
async def apply_colormap(
    request: schemas.ColorMapRequest = Body(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    try:
        # Validate colormap
        if not ColormapHandler.is_valid_colormap(request.colormap):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid colormap: {request.colormap}. Available: {ColormapHandler.AVAILABLE_COLORMAPS}"
            )

        # Check if processing is already in progress
        status = ColorMapProcessor.get_status()
        if status['status'] == 'processing':
            raise HTTPException(
                status_code=409,
                detail=f"Colormap processing already in progress. Current: {status['processed']}/{status['total']}"
            )

        # Get total frame count
        total_frames = db.query(ImageFrame).count()
        if total_frames == 0:
            raise HTTPException(
                status_code=404,
                detail="No frames found in database. Please load data first."
            )

        # Start background processing
        background_tasks.add_task(
            ColorMapProcessor.apply_colormap_batch,
            request.colormap,
            request.batch_size
        )

        return schemas.ColorMapResponse(
            message=f"Started applying '{request.colormap}' colormap to {total_frames} frames",
            total_frames=total_frames,
            colormap_applied=request.colormap,
            processing_status="started"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in apply_colormap endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/colormap/status", response_model=schemas.ColorMapProgress)
async def get_colormap_status():
    status = ColorMapProcessor.get_status()
    return schemas.ColorMapProgress(
        processed=status['processed'],
        total=status['total'],
        status=status['status'],
        current_batch=status['current_batch'],
        total_batches=status['total_batches']
    )


@router.get("/colormaps")
async def get_available_colormaps():
    return {
        "colormaps": ColormapHandler.AVAILABLE_COLORMAPS
    }