"""Payment API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from loguru import logger
from app.services.payment_service import payment_service

router = APIRouter()

class PaymentIntentRequest(BaseModel):
    """Request model for payment intent."""
    amount: float
    currency: str = "usd"
    description: Optional[str] = None
    metadata: Optional[dict] = None

class PaymentConfirmRequest(BaseModel):
    """Request model for payment confirmation."""
    payment_intent_id: str

class RefundRequest(BaseModel):
    """Request model for refund."""
    payment_intent_id: str
    reason: Optional[str] = None

@router.post("/create-intent")
async def create_payment_intent(request: PaymentIntentRequest):
    """Create a Stripe payment intent."""
    try:
        metadata = request.metadata or {}
        if request.description:
            metadata['description'] = request.description
        
        result = await payment_service.create_payment_intent(
            amount=request.amount,
            currency=request.currency,
            metadata=metadata
        )
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail=result.get('error', 'Failed to create payment intent'))
        
        logger.info(f"Payment intent created: {result.get('payment_intent_id')}")
        return result
    
    except Exception as e:
        logger.error(f"Error creating payment intent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/confirm")
async def confirm_payment(request: PaymentConfirmRequest):
    """Confirm payment status."""
    try:
        result = await payment_service.confirm_payment(request.payment_intent_id)
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail="Payment confirmation failed")
        
        logger.info(f"Payment confirmed: {request.payment_intent_id}")
        return result
    
    except Exception as e:
        logger.error(f"Error confirming payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{payment_intent_id}")
async def get_payment_status(payment_intent_id: str):
    """Get payment status."""
    try:
        result = await payment_service.get_payment_status(payment_intent_id)
        
        if not result.get('success'):
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return result
    
    except Exception as e:
        logger.error(f"Error getting payment status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refund")
async def process_refund(request: RefundRequest):
    """Process refund."""
    try:
        result = await payment_service.process_refund(
            request.payment_intent_id,
            request.reason
        )
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail=result.get('error', 'Refund failed'))
        
        logger.info(f"Refund processed: {result.get('refund_id')}")
        return result
    
    except Exception as e:
        logger.error(f"Error processing refund: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/setup-intent")
async def create_setup_intent():
    """Create setup intent for saving payment methods."""
    try:
        result = await payment_service.create_setup_intent()
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail="Failed to create setup intent")
        
        logger.info(f"Setup intent created: {result.get('setup_intent_id')}")
        return result
    
    except Exception as e:
        logger.error(f"Error creating setup intent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def payment_health():
    """Health check for payment service."""
    return {
        "status": "healthy",
        "service": "payment-processor",
        "stripe_configured": bool(payment_service.stripe_secret_key),
    }
