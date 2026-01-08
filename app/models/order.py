# File: app/models/order.py
"""
Order model representing buy/sell orders placed by users.
"""
from datetime import datetime
from app import db
from enum import Enum


class OrderType(str, Enum):
    """Type of order - Buy or Sell"""
    BUY = "BUY"
    SELL = "SELL"


class OrderStyle(str, Enum):
    """
    Style of order execution:
    - MARKET: Execute immediately at current market price
    - LIMIT: Execute only at specified price or better
    """
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderStatus(str, Enum):
    """
    Order lifecycle states:
    - NEW: Just created, not yet sent to exchange
    - PLACED: Sent to exchange, awaiting execution
    - EXECUTED: Successfully completed
    - CANCELLED: Cancelled by user
    """
    NEW = "NEW"
    PLACED = "PLACED"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"


class Order(db.Model):
    """
    Represents a trading order (buy or sell request).
    
    Attributes:
        id: Unique order identifier
        user_id: ID of user who placed the order
        symbol: Trading symbol (e.g., "AAPL")
        order_type: BUY or SELL
        order_style: MARKET or LIMIT
        quantity: Number of shares/units
        price: Limit price (only for LIMIT orders)
        status: Current order status
        created_at: When order was created
        updated_at: When order was last updated
    """
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False, index=True)
    symbol = db.Column(db.String(20), nullable=False, index=True)
    order_type = db.Column(db.Enum(OrderType), nullable=False)
    order_style = db.Column(db.Enum(OrderStyle), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(19, 2), nullable=True)  # Only for LIMIT orders
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.NEW)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    trades = db.relationship('Trade', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id} - {self.order_type.value} {self.quantity} {self.symbol}>'
    
    def to_dict(self):
        """Convert order to dictionary for JSON response"""
        return {
            'id': self.id,
            'userId': self.user_id,
            'symbol': self.symbol,
            'orderType': self.order_type.value,
            'orderStyle': self.order_style.value,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else None,
            'status': self.status.value,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        }