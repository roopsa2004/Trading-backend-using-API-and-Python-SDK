# File: app/services/instrument_service.py
"""
Service layer for instrument-related operations.
Handles business logic for fetching and managing instruments.
"""
from app.models import Instrument
from app.exceptions import InstrumentNotFoundException


class InstrumentService:
    """Service for managing financial instruments"""
    
    @staticmethod
    def get_all_instruments(active_only=True):
        """
        Fetch all tradable instruments.
        
        Args:
            active_only: If True, return only active instruments
            
        Returns:
            List of Instrument objects
        """
        query = Instrument.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        instruments = query.order_by(Instrument.symbol).all()
        return instruments
    
    @staticmethod
    def get_instrument_by_symbol(symbol):
        """
        Get specific instrument by symbol.
        
        Args:
            symbol: Trading symbol (e.g., "AAPL")
            
        Returns:
            Instrument object
            
        Raises:
            InstrumentNotFoundException: If instrument doesn't exist
        """
        instrument = Instrument.query.filter_by(
            symbol=symbol.upper(),
            is_active=True
        ).first()
        
        if not instrument:
            raise InstrumentNotFoundException(symbol)
        
        return instrument
    
    @staticmethod
    def get_instruments_by_type(instrument_type):
        """Get all instruments of a specific type"""
        return Instrument.query.filter_by(
            instrument_type=instrument_type,
            is_active=True
        ).all()