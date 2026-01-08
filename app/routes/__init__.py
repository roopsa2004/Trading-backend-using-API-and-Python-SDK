# File: app/routes/__init__.py
"""API routes initialization"""
from flask import Blueprint

# Create blueprints for each resource
instruments_bp = Blueprint('instruments', __name__)
orders_bp = Blueprint('orders', __name__)
trades_bp = Blueprint('trades', __name__)
portfolio_bp = Blueprint('portfolio', __name__)

# Import routes to register them (this must come AFTER blueprint creation)
from app.routes import instruments, orders, trades, portfolio

__all__ = ['instruments_bp', 'orders_bp', 'trades_bp', 'portfolio_bp']