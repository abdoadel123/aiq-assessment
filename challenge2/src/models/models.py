from sqlalchemy import Column, Integer, Float, JSON, DateTime, Index, String
from sqlalchemy.sql import func
from src.database.connection import Base


class ImageFrame(Base):
    __tablename__ = "image_frames"

    id = Column(Integer, primary_key=True, index=True)
    depth = Column(Float, nullable=False, unique=True, index=True)
    pixels = Column(JSON, nullable=False)
    color_map_pixels = Column(JSON, nullable=True)
    colormap_name = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    colormap_applied_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index('idx_depth_range', 'depth'),
        Index('idx_colormap_status', 'colormap_name'),
    )