# File: app/routes/portfolio.py
"""
Portfolio API endpoints.
Handles retrieval of user holdings.
"""
from flask import jsonify
from app.routes import portfolio_bp
from app.services.portfolio_service import PortfolioService
from app.config import Config


@portfolio_bp.route('/portfolio', methods=['GET'])
def get_portfolio():
    """
    Get user's current portfolio holdings.
    
    Returns:
        200: Portfolio details with current values
        
    Example:
        GET /api/v1/portfolio
        
    Response:
        {
            "holdings": [
                {
                    "symbol": "AAPL",
                    "quantity": 10,
                    "averagePrice": 150.00,
                    "totalInvested": 1500.00,
                    "currentValue": 1525.00,
                    "profitLoss": 25.00,
                    "profitLossPercentage": 1.67
                }
            ],
            "totalInvested": 1500.00,
            "totalCurrentValue": 1525.00,
            "totalProfitLoss": 25.00
        }
    """
    try:
        user_id = Config.DEFAULT_USER_ID
        holdings = PortfolioService.get_user_portfolio(user_id)
        
        # Calculate totals
        total_invested = sum(h.get('totalInvested', 0) for h in holdings)
        total_current = sum(h.get('currentValue', 0) for h in holdings)
        total_pl = total_current - total_invested
        
        return jsonify({
            'holdings': holdings,
            'totalInvested': float(total_invested),
            'totalCurrentValue': float(total_current),
            'totalProfitLoss': float(total_pl),
            'count': len(holdings)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500