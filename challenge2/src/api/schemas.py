from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ResizeRequest(BaseModel):
    csv_path: str = Field(default="/app/data.csv", description="Path to the CSV file")
    target_width: int = Field(default=150, description="Target width for resizing")


class ResizeResponse(BaseModel):
    message: str
    frames_processed: int
    target_width: int


class FrameResponse(BaseModel):
    id: int
    depth: float
    pixels: List[int]  # Resized pixels
    color_map_pixels: Optional[List[List[int]]] = None  # RGB values if colormap applied
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
    colormap: str = Field(default="viridis", description="Name of the colormap to apply")
    batch_size: int = Field(default=100, description="Batch size for processing")


class ColorMapResponse(BaseModel):
    message: str
    total_frames: int
    colormap_applied: str
    processing_status: str  # 'started', 'in_progress', 'completed'

class ColorMapProgress(BaseModel):
    processed: int
    total: int
    status: str
    current_batch: int
    total_batches: int