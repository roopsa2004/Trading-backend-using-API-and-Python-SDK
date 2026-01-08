# File: app/services/order_service.py
"""
Service layer for order management.
Handles order creation, validation, and status updates.
"""
from decimal import Decimal
from app import db
from app.models import Order, OrderType, OrderStyle, OrderStatus
from app.services.instrument_service import InstrumentService
from app.services.portfolio_service import PortfolioService
from app.exceptions import InvalidOrderException, InsufficientHoldingsException


class OrderService:
    """Service for managing trading orders"""
    
    @staticmethod
    def validate_order(symbol, order_type, order_style, quantity, price, user_id):
        """
        Validate order parameters before creation.
        
        Validation rules:
        1. Quantity must be > 0
        2. LIMIT orders must have a price
        3. Instrument must exist and be tradable
        4. For SELL orders, user must have sufficient holdings
        
        Args:
            symbol: Trading symbol
            order_type: BUY or SELL
            order_style: MARKET or LIMIT
            quantity: Number of shares
            price: Limit price (can be None for MARKET orders)
            user_id: User placing the order
            
        Raises:
            InvalidOrderException: If validation fails
            InsufficientHoldingsException: If selling more than owned
        """
        # Validate quantity
        if quantity <= 0:
            raise InvalidOrderException("Quantity must be greater than 0")
        
        # Validate price for LIMIT orders
        if order_style == OrderStyle.LIMIT and (price is None or price <= 0):
            raise InvalidOrderException("LIMIT orders must have a valid price")
        
        # Validate instrument exists
        instrument = InstrumentService.get_instrument_by_symbol(symbol)
        
        # For SELL orders, check if user has sufficient holdings
        if order_type == OrderType.SELL:
            portfolio = PortfolioService.get_user_holding(user_id, symbol)
            if not portfolio or portfolio.quantity < quantity:
                available = portfolio.quantity if portfolio else 0
                raise InsufficientHoldingsException(symbol, available, quantity)
        
        return instrument
    
    @staticmethod
    def create_order(user_id, symbol, order_type, order_style, quantity, price=None):
        """
        Create a new order.
        
        Args:
            user_id: User placing the order
            symbol: Trading symbol
            order_type: BUY or SELL
            order_style: MARKET or LIMIT
            quantity: Number of shares
            price: Limit price (optional for MARKET orders)
            
        Returns:
            Created Order object
        """
        # Validate order
        instrument = OrderService.validate_order(
            symbol, order_type, order_style, quantity, price, user_id
        )
        
        # Create order
        order = Order(
            user_id=user_id,
            symbol=instrument.symbol,
            order_type=order_type,
            order_style=order_style,
            quantity=quantity,
            price=Decimal(str(price)) if price else None,
            status=OrderStatus.NEW
        )
        
        db.session.add(order)
        db.session.commit()
        
        return order
    
    @staticmethod
    def get_order_by_id(order_id):
        """Get order by ID"""
        from app.exceptions import OrderNotFoundException
        
        order = Order.query.get(order_id)
        if not order:
            raise OrderNotFoundException(order_id)
        
        return order
    
    @staticmethod
    def get_user_orders(user_id, status=None):
        """
        Get all orders for a user, optionally filtered by status.
        
        Args:
            user_id: User ID
            status: Optional OrderStatus to filter by
            
        Returns:
            List of Order objects
        """
        query = Order.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(Order.created_at.desc()).all()
    
    @staticmethod
    def update_order_status(order_id, new_status):
        """Update order status"""
        order = OrderService.get_order_by_id(order_id)
        order.status = new_status
        db.session.commit()
        return order
    
    @staticmethod
    def cancel_order(order_id):
        """
        Cancel an order.
        Only NEW or PLACED orders can be cancelled.
        """
        order = OrderService.get_order_by_id(order_id)
        
        if order.status in [OrderStatus.EXECUTED, OrderStatus.CANCELLED]:
            raise InvalidOrderException(
                f"Cannot cancel order in {order.status.value} status"
            )
        
        order.status = OrderStatus.CANCELLED
        db.session.commit()
        return order