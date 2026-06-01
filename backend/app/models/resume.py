"""Resume model."""

from sqlalchemy import Column, String, DateTime, Float, Boolean, JSON, Text, Integer
from app.models.base import Base
from datetime import datetime
import uuid

class Resume(Base):
    """Resume model for storing resume data and processing information."""
    
    __tablename__ = "resumes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    extracted_data = Column(JSON, nullable=True)
    optimized_content = Column(Text, nullable=True)
    optimized_file_path = Column(String, nullable=True)
    job_description = Column(Text, nullable=True)
    ats_score = Column(Float, nullable=True, default=0.0)
    suggestions = Column(JSON, nullable=True)
    is_paid = Column(Boolean, default=False)
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Resume {self.id}>"
