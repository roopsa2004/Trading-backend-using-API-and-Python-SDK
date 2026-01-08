# File: app/exceptions/custom_exceptions.py
"""
Custom exception classes for business logic errors.
These provide meaningful error messages to API consumers.
"""


class TradingPlatformException(Exception):
    """Base exception for all trading platform errors"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """Convert exception to dictionary for JSON response"""
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['status'] = self.status_code
        return rv


class InvalidOrderException(TradingPlatformException):
    """
    Raised when order validation fails.
    Examples:
    - Quantity <= 0
    - Limit order without price
    - Invalid symbol
    """
    
    def __init__(self, message):
        super().__init__(message, status_code=400)


class InsufficientHoldingsException(TradingPlatformException):
    """
    Raised when user tries to sell more shares than they own.
    Example: User owns 10 shares but tries to sell 20.
    """
    
    def __init__(self, symbol, available, requested):
        message = (
            f"Insufficient holdings for {symbol}. "
            f"Available: {available}, Requested: {requested}"
        )
        super().__init__(message, status_code=400)
        self.payload = {
            'symbol': symbol,
            'available': available,
            'requested': requested
        }


class InsufficientFundsException(TradingPlatformException):
    """
    Raised when user doesn't have enough funds to complete purchase.
    Note: In this simplified version, we're not tracking actual funds,
    but this is included for completeness.
    """
    
    def __init__(self, required, available):
        message = f"Insufficient funds. Required: {required}, Available: {available}"
        super().__init__(message, status_code=400)
        self.payload = {
            'required': float(required),
            'available': float(available)
        }


class InstrumentNotFoundException(TradingPlatformException):
    """
    Raised when requested instrument doesn't exist or is not tradable.
    """
    
    def __init__(self, symbol):
        message = f"Instrument '{symbol}' not found or not tradable"
        super().__init__(message, status_code=404)
        self.payload = {'symbol': symbol}


class OrderNotFoundException(TradingPlatformException):
    """
    Raised when requested order doesn't exist.
    """
    
    def __init__(self, order_id):
        message = f"Order {order_id} not found"
        super().__init__(message, status_code=404)
        self.payload = {'orderId': order_id}