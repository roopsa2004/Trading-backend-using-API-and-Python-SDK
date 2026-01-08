# File: app/services/execution_engine.py
"""
Order execution engine.
Simulates order execution and creates trades.
"""
from app import db
from app.models import OrderStyle, OrderStatus
from app.services.instrument_service import InstrumentService
from app.services.trade_service import TradeService
from app.services.portfolio_service import PortfolioService
from app.services.order_service import OrderService


class OrderExecutionEngine:
    """
    Simulates order execution logic.
    
    In a real trading system, this would interface with exchanges.
    Here, we simulate immediate execution for simplicity.
    """
    
    @staticmethod
    def execute_order(order):
        """
        Execute an order and create corresponding trade.
        
        Execution logic:
        - MARKET orders: Execute immediately at last traded price
        - LIMIT orders: Execute at limit price (simplified simulation)
        
        Args:
            order: Order object to execute
            
        Returns:
            Created Trade object
        """
        # Get current instrument price
        instrument = InstrumentService.get_instrument_by_symbol(order.symbol)
        
        # Determine execution price
        if order.order_style == OrderStyle.MARKET:
            execution_price = instrument.last_traded_price
        else:  # LIMIT order
            # In real system, check if limit price is achievable
            # For simulation, execute at limit price
            execution_price = order.price
        
        # Update order status to PLACED then EXECUTED
        order.status = OrderStatus.PLACED
        db.session.commit()
        
        # Create trade
        trade = TradeService.create_trade(order, execution_price)
        
        # Update portfolio
        PortfolioService.update_portfolio_after_trade(trade)
        
        # Update order status to EXECUTED
        order.status = OrderStatus.EXECUTED
        db.session.commit()
        
        return trade
    
    @staticmethod
    def execute_market_order(order):
        """Execute market order immediately"""
        return OrderExecutionEngine.execute_order(order)