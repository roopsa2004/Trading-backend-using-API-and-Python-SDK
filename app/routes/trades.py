# File: app/routes/trades.py
"""
Trade API endpoints.
Handles retrieval of executed trades.
"""
from flask import jsonify, request
from app.routes import trades_bp
from app.services.trade_service import TradeService
from app.config import Config


@trades_bp.route('/trades', methods=['GET'])
def get_trades():
    """
    Get all executed trades for the user.
    
    Query Parameters:
        symbol: Optional symbol filter
        
    Returns:
        200: List of trades
        
    Example:
        GET /api/v1/trades?symbol=AAPL
        
    Response:
        {
            "trades": [
                {
                    "id": 1,
                    "symbol": "AAPL",
                    "tradeType": "BUY",
                    "quantity": 10,
                    "executedPrice": 150.25,
                    "totalValue": 1502.50,
                    "executedAt": "2024-01-15T10:30:00"
                }
            ],
            "count": 1
        }
    """
    try:
        user_id = Config.DEFAULT_USER_ID
        symbol = request.args.get('symbol')
        
        if symbol:
            trades = TradeService.get_trades_by_symbol(user_id, symbol.upper())
        else:
            trades = TradeService.get_user_trades(user_id)
        
        return jsonify({
            'trades': [trade.to_dict() for trade in trades],
            'count': len(trades)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500