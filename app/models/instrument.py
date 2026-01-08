# File: app/models/instrument.py
"""
Instrument model representing tradable financial instruments.
Example: Stocks (AAPL, GOOGL), Options, Futures, etc.
"""
from datetime import datetime
from app import db
from enum import Enum


class InstrumentType(str, Enum):
    """Types of financial instruments"""
    EQUITY = "EQUITY"        # Stocks
    FUTURES = "FUTURES"      # Futures contracts
    OPTIONS = "OPTIONS"      # Options contracts
    COMMODITY = "COMMODITY"  # Commodities
    CURRENCY = "CURRENCY"    # Forex


class Instrument(db.Model):
    """
    Represents a tradable financial instrument.
    
    Attributes:
        id: Unique identifier
        symbol: Trading symbol (e.g., "AAPL")
        name: Full name (e.g., "Apple Inc.")
        exchange: Exchange where it trades (e.g., "NASDAQ")
        instrument_type: Type of instrument (EQUITY, OPTIONS, etc.)
        last_traded_price: Current/last traded price
        is_active: Whether instrument is currently tradable
    """
    __tablename__ = 'instruments'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    exchange = db.Column(db.String(50), nullable=False)
    instrument_type = db.Column(db.Enum(InstrumentType), nullable=False, default=InstrumentType.EQUITY)
    last_traded_price = db.Column(db.Numeric(19, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Instrument {self.symbol} - {self.name}>'
    
    def to_dict(self):
        """Convert instrument to dictionary for JSON response"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'exchange': self.exchange,
            'instrumentType': self.instrument_type.value,
            'lastTradedPrice': float(self.last_traded_price),
            'isActive': self.is_active
        }