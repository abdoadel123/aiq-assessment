from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import Optional
from src.services import DataLoader, ColorMapProcessor, FrameService
from src.utils.colormap import ColormapHandler
from . import schemas
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["images"])


@router.post("/resize", response_model=schemas.ResizeResponse)
async def resize_images(
    request: schemas.ResizeRequest = Body(...),
    data_loader: DataLoader = Depends()
):
    try:
        image_id, frames_processed = data_loader.load_resize_and_save(
            csv_path="data.csv",
            target_width=request.target_width
        )

        return schemas.ResizeResponse(
            message=f"Successfully processed and resized {frames_processed} frames",
            image_id=image_id,
            frames_processed=frames_processed,
            target_width=request.target_width
        )
    except Exception as e:
        logger.error(f"Error in resize endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/frames", response_model=schemas.FramesQueryResponse)
async def get_frames(
    image_id: int = Query(..., description="Image ID"),
    depth_min: Optional[float] = Query(None, description="Minimum depth value"),
    depth_max: Optional[float] = Query(None, description="Maximum depth value"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, le=1000, description="Items per page (max 1000)"),
    coloredmap: Optional[bool] = Query(None, description="Return colormap pixels (true) or grayscale pixels (false)"),
    frame_service: FrameService = Depends()
):
    try:
        frames, total, total_pages = frame_service.get_frames_with_filters(
            image_id=image_id,
            depth_min=depth_min,
            depth_max=depth_max,
            page=page,
            per_page=per_page,
            coloredmap=coloredmap
        )

        if total == 0:
            return schemas.FramesQueryResponse(
                frames=[],
                count=0,
                total=0,
                page=page,
                per_page=per_page,
                total_pages=0
            )

        frame_responses = []
        if coloredmap is True:
            frame_responses = [
                schemas.FrameResponse(
                    id=frame.id,
                    image_id=frame.image_id,
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
                    image_id=frame.image_id,
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_frames endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/colormap/apply", response_model=schemas.ColorMapResponse)
async def apply_colormap(
    request: schemas.ColorMapRequest = Body(...),
    colormap_service: ColorMapProcessor = Depends()
):
    try:
        result = colormap_service.apply_colormap_to_image(
            request.image_id,
            request.colormap,
            request.batch_size
        )

        return schemas.ColorMapResponse(
            message=f"Successfully applied '{request.colormap}' colormap",
            image_id=request.image_id,
            processed=result['processed'],
            total=result['total'],
            colormap_applied=request.colormap
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in apply_colormap endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/colormaps")
async def get_available_colormaps():
    return {
        "colormaps": ColormapHandler.AVAILABLE_COLORMAPS
    }