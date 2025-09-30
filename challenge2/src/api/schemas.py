from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ResizeRequest(BaseModel):
    target_width: int = Field(default=150, description="Target width for resizing")


class ResizeResponse(BaseModel):
    message: str
    image_id: int
    frames_processed: int
    target_width: int


class FrameResponse(BaseModel):
    id: int
    image_id: int
    depth: float
    pixels: List[int]
    color_map_pixels: Optional[List[List[int]]] = None
    colormap_name: Optional[str] = None
    created_at: datetime
    colormap_applied_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FramesQueryResponse(BaseModel):
    frames: List[FrameResponse]
    count: int
    total: int
    page: int
    per_page: int
    total_pages: int


class ColorMapRequest(BaseModel):
    image_id: int = Field(description="ID of the image to apply colormap to")
    colormap: str = Field(default="viridis", description="Name of the colormap to apply")
    batch_size: int = Field(default=100, description="Batch size for processing")


class ColorMapResponse(BaseModel):
    message: str
    image_id: int
    processed: int
    total: int
    colormap_applied: str