from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.connection import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    target_width = Column(Integer, nullable=False)
    total_frames = Column(Integer, nullable=False, default=0)
    csv_source = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    frames = relationship("ImageFrame", back_populates="image", cascade="all, delete-orphan")