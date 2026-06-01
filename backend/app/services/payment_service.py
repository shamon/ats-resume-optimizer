"""Enhanced payment processing service with Stripe integration."""

from typing import Dict, Optional
from loguru import logger
import stripe
import os
from datetime import datetime

class PaymentService:
    """Handle payment processing through Stripe."""
    
    def __init__(self):
        """Initialize Stripe API."""
        self.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY", "")
        self.stripe_publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
        
        if self.stripe_secret_key:
            stripe.api_key = self.stripe_secret_key
    
    async def create_payment_intent(
        self,
        amount: float,
        currency: str = "usd",
        metadata: dict = None
    ) -> Dict:
        """Create a Stripe payment intent."""
        try:
            if not self.stripe_secret_key:
                logger.warning("Stripe API key not configured")
                return {
                    'success': False,
                    'error': 'Payment service not configured',
                }
            
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                payment_method_types=['card'],
                metadata=metadata or {},
            )
            
            logger.info(f"Payment intent created: {intent.id}")
            return {
                'success': True,
                'payment_intent_id': intent.id,
                'client_secret': intent.client_secret,
                'amount': amount,
                'currency': currency,
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating payment intent: {e}")
            return {
                'success': False,
                'error': f"Payment error: {str(e)}",
            }
        except Exception as e:
            logger.error(f"Error creating payment intent: {e}")
            return {
                'success': False,
                'error': str(e),
            }
    
    async def confirm_payment(self, payment_intent_id: str) -> Dict:
        """Confirm payment status."""
        try:
            if not self.stripe_secret_key:
                return {'success': False, 'error': 'Payment service not configured'}
            
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'success': intent.status == 'succeeded',
                'status': intent.status,
                'amount': intent.amount / 100,
                'currency': intent.currency,
                'payment_intent_id': intent.id,
                'client_secret': intent.client_secret,
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error confirming payment: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Error confirming payment: {e}")
            return {'success': False, 'error': str(e)}
    
    async def process_refund(
        self,
        payment_intent_id: str,
        reason: str = None
    ) -> Dict:
        """Process a refund for a payment."""
        try:
            if not self.stripe_secret_key:
                return {'success': False, 'error': 'Payment service not configured'}
            
            # Get the payment intent to find the charge
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if not intent.charges.data:
                return {'success': False, 'error': 'No charge found for this payment'}
            
            charge_id = intent.charges.data[0].id
            
            # Create refund
            refund = stripe.Refund.create(
                charge=charge_id,
                reason=reason or 'requested_by_customer',
            )
            
            logger.info(f"Refund processed: {refund.id}")
            return {
                'success': True,
                'refund_id': refund.id,
                'amount': refund.amount / 100,
                'status': refund.status,
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error processing refund: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Error processing refund: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_payment_status(self, payment_intent_id: str) -> Dict:
        """Get detailed payment status."""
        try:
            if not self.stripe_secret_key:
                return {'success': False, 'error': 'Payment service not configured'}
            
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            payment_data = {
                'success': True,
                'payment_intent_id': intent.id,
                'status': intent.status,
                'amount': intent.amount / 100,
                'currency': intent.currency,
                'created': datetime.fromtimestamp(intent.created).isoformat(),
                'client_secret': intent.client_secret,
            }
            
            if intent.charges.data:
                charge = intent.charges.data[0]
                payment_data['charge'] = {
                    'id': charge.id,
                    'status': charge.status,
                    'paid': charge.paid,
                }
            
            return payment_data
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error getting payment status: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Error getting payment status: {e}")
            return {'success': False, 'error': str(e)}
    
    async def create_setup_intent(self) -> Dict:
        """Create a setup intent for saving payment methods."""
        try:
            if not self.stripe_secret_key:
                return {'success': False, 'error': 'Payment service not configured'}
            
            intent = stripe.SetupIntent.create()
            
            return {
                'success': True,
                'setup_intent_id': intent.id,
                'client_secret': intent.client_secret,
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating setup intent: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Error creating setup intent: {e}")
            return {'success': False, 'error': str(e)}

payment_service = PaymentService()
