# File: app/models/trade.py
"""
Trade model representing executed orders.
When an order is executed, a trade record is created.
"""
from datetime import datetime
from app import db
from app.models.order import OrderType


class Trade(db.Model):
    """
    Represents a completed trade (executed order).
    
    Attributes:
        id: Unique trade identifier
        order_id: Reference to the original order
        user_id: ID of user who made the trade
        symbol: Trading symbol
        trade_type: BUY or SELL
        quantity: Number of shares/units traded
        executed_price: Price at which trade was executed
        total_value: Total transaction value (quantity * price)
        executed_at: When trade was executed
    """
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    user_id = db.Column(db.String(50), nullable=False, index=True)
    symbol = db.Column(db.String(20), nullable=False, index=True)
    trade_type = db.Column(db.Enum(OrderType), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    executed_price = db.Column(db.Numeric(19, 2), nullable=False)
    total_value = db.Column(db.Numeric(19, 2), nullable=False)
    executed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Trade {self.id} - {self.trade_type.value} {self.quantity} {self.symbol} @ {self.executed_price}>'
    
    def to_dict(self):
        """Convert trade to dictionary for JSON response"""
        return {
            'id': self.id,
            'orderId': self.order_id,
            'userId': self.user_id,
            'symbol': self.symbol,
            'tradeType': self.trade_type.value,
            'quantity': self.quantity,
            'executedPrice': float(self.executed_price),
            'totalValue': float(self.total_value),
            'executedAt': self.executed_at.isoformat()
        }