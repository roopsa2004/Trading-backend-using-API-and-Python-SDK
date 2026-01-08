# File: app/services/portfolio_service.py
"""
Service layer for portfolio management.
Handles user holdings and position calculations.
"""
from decimal import Decimal
from app import db
from app.models import Portfolio, OrderType
from app.services.instrument_service import InstrumentService


class PortfolioService:
    """Service for managing user portfolio"""
    
    @staticmethod
    def get_user_portfolio(user_id):
        """
        Get complete portfolio for a user with current values.
        
        Returns:
            List of Portfolio objects with current market values
        """
        holdings = Portfolio.query.filter_by(user_id=user_id).all()
        
        # Enrich with current prices
        enriched_holdings = []
        for holding in holdings:
            try:
                instrument = InstrumentService.get_instrument_by_symbol(holding.symbol)
                holding_dict = holding.to_dict(current_price=instrument.last_traded_price)
                enriched_holdings.append(holding_dict)
            except:
                # If instrument not found, just add without current value
                enriched_holdings.append(holding.to_dict())
        
        return enriched_holdings
    
    @staticmethod
    def get_user_holding(user_id, symbol):
        """Get user's holding for a specific symbol"""
        return Portfolio.query.filter_by(
            user_id=user_id,
            symbol=symbol
        ).first()
    
    @staticmethod
    def update_portfolio_after_trade(trade):
        """
        Update portfolio after a trade is executed.
        
        For BUY: Increase quantity and update average price
        For SELL: Decrease quantity
        
        Args:
            trade: Trade object
        """
        holding = PortfolioService.get_user_holding(trade.user_id, trade.symbol)
        
        if trade.trade_type == OrderType.BUY:
            if holding:
                # Update existing holding
                # Calculate new average price: (old_value + new_value) / total_quantity
                old_value = holding.average_price * holding.quantity
                new_value = trade.executed_price * trade.quantity
                new_quantity = holding.quantity + trade.quantity
                
                holding.average_price = (old_value + new_value) / new_quantity
                holding.quantity = new_quantity
                holding.total_invested = holding.average_price * holding.quantity
            else:
                # Create new holding
                holding = Portfolio(
                    user_id=trade.user_id,
                    symbol=trade.symbol,
                    quantity=trade.quantity,
                    average_price=trade.executed_price,
                    total_invested=trade.total_value
                )
                db.session.add(holding)
        
        elif trade.trade_type == OrderType.SELL:
            if holding:
                holding.quantity -= trade.quantity
                
                # If all sold, remove from portfolio
                if holding.quantity == 0:
                    db.session.delete(holding)
                else:
                    holding.total_invested = holding.average_price * holding.quantity
        
        db.session.commit()
        return holding