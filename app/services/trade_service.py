# File: app/services/trade_service.py
"""
Service layer for trade management.
Handles creation and retrieval of executed trades.
"""
from decimal import Decimal
from app import db
from app.models import Trade, OrderType


class TradeService:
    """Service for managing executed trades"""
    
    @staticmethod
    def create_trade(order, executed_price):
        """
        Create a trade record for an executed order.
        
        Args:
            order: Order object that was executed
            executed_price: Price at which order was executed
            
        Returns:
            Created Trade object
        """
        executed_price_decimal = Decimal(str(executed_price))
        total_value = executed_price_decimal * order.quantity
        
        trade = Trade(
            order_id=order.id,
            user_id=order.user_id,
            symbol=order.symbol,
            trade_type=order.order_type,
            quantity=order.quantity,
            executed_price=executed_price_decimal,
            total_value=total_value
        )
        
        db.session.add(trade)
        db.session.commit()
        
        return trade
    
    @staticmethod
    def get_user_trades(user_id):
        """Get all trades for a user"""
        return Trade.query.filter_by(user_id=user_id).order_by(
            Trade.executed_at.desc()
        ).all()
    
    @staticmethod
    def get_trades_by_symbol(user_id, symbol):
        """Get all trades for a specific symbol"""
        return Trade.query.filter_by(
            user_id=user_id,
            symbol=symbol
        ).order_by(Trade.executed_at.desc()).all()