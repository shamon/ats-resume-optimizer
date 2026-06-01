"""Payment model."""

from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from app.models.base import Base
from datetime import datetime
import uuid

class Payment(Base):
    """Payment transaction model."""
    
    __tablename__ = "payments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String, ForeignKey('resumes.id'), nullable=False)
    stripe_transaction_id = Column(String, unique=True, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="pending")  # pending, completed, failed, refunded
    refunded = Column(Boolean, default=False)
    refund_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Payment {self.id}>"
