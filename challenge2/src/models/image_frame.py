from sqlalchemy import Column, Integer, Float, JSON, DateTime, Index, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.connection import Base


class ImageFrame(Base):
    __tablename__ = "image_frames"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey('images.id', ondelete='CASCADE'), nullable=False, index=True)
    depth = Column(Float, nullable=False, index=True)
    pixels = Column(JSON, nullable=False)
    color_map_pixels = Column(JSON, nullable=True)
    colormap_name = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    colormap_applied_at = Column(DateTime(timezone=True), nullable=True)

    image = relationship("Image", back_populates="frames")

    __table_args__ = (
        Index('idx_image_depth', 'image_id', 'depth'),
        Index('idx_colormap_status', 'image_id', 'colormap_name'),
    )