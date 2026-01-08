# File: app/models/portfolio.py
"""
Portfolio model representing user's current holdings.
Updated automatically when trades are executed.
"""
from datetime import datetime
from app import db


class Portfolio(db.Model):
    """
    Represents user's holdings for a specific instrument.
    
    Attributes:
        id: Unique identifier
        user_id: ID of user who owns the holdings
        symbol: Trading symbol
        quantity: Total number of shares/units owned
        average_price: Average purchase price
        total_invested: Total amount invested
        updated_at: When holdings were last updated
    """
    __tablename__ = 'portfolio'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False, index=True)
    symbol = db.Column(db.String(20), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    average_price = db.Column(db.Numeric(19, 2), nullable=False, default=0)
    total_invested = db.Column(db.Numeric(19, 2), nullable=False, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Composite unique constraint: one portfolio entry per user per symbol
    __table_args__ = (
        db.UniqueConstraint('user_id', 'symbol', name='unique_user_symbol'),
    )
    
    def __repr__(self):
        return f'<Portfolio {self.user_id} - {self.quantity} {self.symbol}>'
    
    def calculate_current_value(self, current_price):
        """Calculate current market value of holdings"""
        return float(self.quantity) * float(current_price)
    
    def to_dict(self, current_price=None):
        """Convert portfolio to dictionary for JSON response"""
        result = {
            'id': self.id,
            'userId': self.user_id,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'averagePrice': float(self.average_price),
            'totalInvested': float(self.total_invested),
            'updatedAt': self.updated_at.isoformat()
        }
        
        if current_price:
            result['currentValue'] = self.calculate_current_value(current_price)
            result['profitLoss'] = result['currentValue'] - float(self.total_invested)
            result['profitLossPercentage'] = (
                (result['profitLoss'] / float(self.total_invested)) * 100 
                if self.total_invested > 0 else 0
            )
        
        return result