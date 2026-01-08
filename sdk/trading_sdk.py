# File: sdk/trading_sdk.py
"""
Trading Platform SDK - Python Client
A wrapper around the Trading Platform REST API for easy integration.

Usage Example:
    from sdk.trading_sdk import TradingSDK
    
    # Initialize SDK
    sdk = TradingSDK(base_url='http://localhost:5000')
    
    # Get instruments
    instruments = sdk.get_instruments()
    
    # Place an order
    order = sdk.place_order('AAPL', 'BUY', 'MARKET', 10)
    
    # Get portfolio
    portfolio = sdk.get_portfolio()
"""

import requests
from typing import Optional, List, Dict, Any
import json


class TradingSDKException(Exception):
    """Exception raised for SDK errors"""
    
    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class TradingSDK:
    """
    Python SDK for Trading Platform API.
    Provides simple methods to interact with the trading platform.
    """
    
    def __init__(self, base_url: str = 'http://localhost:5000', timeout: int = 30):
        """
        Initialize the Trading SDK.
        
        Args:
            base_url: Base URL of the trading platform API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_prefix = '/api/v1'
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, 
                     data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            data: Request body data
            params: Query parameters
            
        Returns:
            Response JSON data
            
        Raises:
            TradingSDKException: If request fails
        """
        url = f"{self.base_url}{self.api_prefix}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            # Try to parse JSON response
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {'error': 'Invalid JSON response'}
            
            # Check for errors
            if response.status_code >= 400:
                error_msg = response_data.get('error', 'Unknown error')
                raise TradingSDKException(
                    message=error_msg,
                    status_code=response.status_code,
                    response=response_data
                )
            
            return response_data
            
        except requests.exceptions.RequestException as e:
            raise TradingSDKException(f"Request failed: {str(e)}")
    
    # ==================== INSTRUMENT METHODS ====================
    
    def get_instruments(self, active_only: bool = True) -> List[Dict]:
        """
        Get all tradable instruments.
        
        Args:
            active_only: If True, return only active instruments
            
        Returns:
            List of instrument dictionaries
            
        Example:
            instruments = sdk.get_instruments()
            for inst in instruments:
                print(f"{inst['symbol']}: ${inst['lastTradedPrice']}")
        """
        params = {'active_only': str(active_only).lower()}
        response = self._make_request('GET', '/instruments', params=params)
        return response.get('instruments', [])
    
    def get_instrument(self, symbol: str) -> Dict:
        """
        Get specific instrument by symbol.
        
        Args:
            symbol: Trading symbol (e.g., 'AAPL')
            
        Returns:
            Instrument dictionary
            
        Example:
            instrument = sdk.get_instrument('AAPL')
            print(f"Price: ${instrument['lastTradedPrice']}")
        """
        return self._make_request('GET', f'/instruments/{symbol.upper()}')
    
    # ==================== ORDER METHODS ====================
    
    def place_order(self, symbol: str, order_type: str, order_style: str,
                   quantity: int, price: Optional[float] = None) -> Dict:
        """
        Place a new order.
        
        Args:
            symbol: Trading symbol (e.g., 'AAPL')
            order_type: 'BUY' or 'SELL'
            order_style: 'MARKET' or 'LIMIT'
            quantity: Number of shares (must be > 0)
            price: Limit price (required for LIMIT orders)
            
        Returns:
            Dictionary containing order and trade details
            
        Example:
            # Market order
            result = sdk.place_order('AAPL', 'BUY', 'MARKET', 10)
            
            # Limit order
            result = sdk.place_order('AAPL', 'BUY', 'LIMIT', 10, price=150.00)
        """
        data = {
            'symbol': symbol.upper(),
            'orderType': order_type.upper(),
            'orderStyle': order_style.upper(),
            'quantity': quantity
        }
        
        if price is not None:
            data['price'] = price
        
        return self._make_request('POST', '/orders', data=data)
    
    def place_buy_order(self, symbol: str, quantity: int, 
                       price: Optional[float] = None) -> Dict:
        """
        Convenience method to place a BUY order.
        
        Args:
            symbol: Trading symbol
            quantity: Number of shares
            price: If provided, creates LIMIT order; otherwise MARKET order
            
        Returns:
            Order and trade details
            
        Example:
            # Market buy
            result = sdk.place_buy_order('AAPL', 10)
            
            # Limit buy
            result = sdk.place_buy_order('AAPL', 10, price=150.00)
        """
        order_style = 'LIMIT' if price else 'MARKET'
        return self.place_order(symbol, 'BUY', order_style, quantity, price)
    
    def place_sell_order(self, symbol: str, quantity: int,
                        price: Optional[float] = None) -> Dict:
        """
        Convenience method to place a SELL order.
        
        Args:
            symbol: Trading symbol
            quantity: Number of shares
            price: If provided, creates LIMIT order; otherwise MARKET order
            
        Returns:
            Order and trade details
            
        Example:
            # Market sell
            result = sdk.place_sell_order('AAPL', 10)
            
            # Limit sell
            result = sdk.place_sell_order('AAPL', 10, price=160.00)
        """
        order_style = 'LIMIT' if price else 'MARKET'
        return self.place_order(symbol, 'SELL', order_style, quantity, price)
    
    def get_order(self, order_id: int) -> Dict:
        """
        Get order details by ID.
        
        Args:
            order_id: Order ID
            
        Returns:
            Order dictionary
            
        Example:
            order = sdk.get_order(1)
            print(f"Status: {order['status']}")
        """
        return self._make_request('GET', f'/orders/{order_id}')
    
    def get_orders(self, status: Optional[str] = None) -> List[Dict]:
        """
        Get all orders, optionally filtered by status.
        
        Args:
            status: Optional status filter ('NEW', 'PLACED', 'EXECUTED', 'CANCELLED')
            
        Returns:
            List of order dictionaries
            
        Example:
            # Get all orders
            all_orders = sdk.get_orders()
            
            # Get only executed orders
            executed = sdk.get_orders(status='EXECUTED')
        """
        params = {}
        if status:
            params['status'] = status.upper()
        
        response = self._make_request('GET', '/orders', params=params)
        return response.get('orders', [])
    
    def cancel_order(self, order_id: int) -> Dict:
        """
        Cancel an order.
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            Cancelled order details
            
        Example:
            result = sdk.cancel_order(1)
            print(result['message'])
        """
        return self._make_request('POST', f'/orders/{order_id}/cancel')
    
    # ==================== TRADE METHODS ====================
    
    def get_trades(self, symbol: Optional[str] = None) -> List[Dict]:
        """
        Get executed trades, optionally filtered by symbol.
        
        Args:
            symbol: Optional symbol filter
            
        Returns:
            List of trade dictionaries
            
        Example:
            # Get all trades
            all_trades = sdk.get_trades()
            
            # Get trades for specific symbol
            aapl_trades = sdk.get_trades(symbol='AAPL')
        """
        params = {}
        if symbol:
            params['symbol'] = symbol.upper()
        
        response = self._make_request('GET', '/trades', params=params)
        return response.get('trades', [])
    
    # ==================== PORTFOLIO METHODS ====================
    
    def get_portfolio(self) -> Dict:
        """
        Get current portfolio holdings.
        
        Returns:
            Dictionary containing holdings and summary
            
        Example:
            portfolio = sdk.get_portfolio()
            print(f"Total Value: ${portfolio['totalCurrentValue']}")
            
            for holding in portfolio['holdings']:
                print(f"{holding['symbol']}: {holding['quantity']} shares")
        """
        return self._make_request('GET', '/portfolio')
    
    def get_holding(self, symbol: str) -> Optional[Dict]:
        """
        Get holding for a specific symbol.
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Holding dictionary or None if not found
            
        Example:
            holding = sdk.get_holding('AAPL')
            if holding:
                print(f"Quantity: {holding['quantity']}")
        """
        portfolio = self.get_portfolio()
        holdings = portfolio.get('holdings', [])
        
        for holding in holdings:
            if holding['symbol'] == symbol.upper():
                return holding
        
        return None
    
    # ==================== HELPER METHODS ====================
    
    def health_check(self) -> Dict:
        """
        Check API health status.
        
        Returns:
            Health status dictionary
        """
        url = f"{self.base_url}/health"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return response.json()
        except Exception as e:
            raise TradingSDKException(f"Health check failed: {str(e)}")
    
    def close(self):
        """Close the HTTP session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()