# File: app/routes/orders.py
"""
Order API endpoints.
Handles order placement, status checks, and cancellations.
"""
from flask import jsonify, request
from app.routes import orders_bp
from app.services.order_service import OrderService
from app.services.execution_engine import OrderExecutionEngine
from app.models import OrderType, OrderStyle, OrderStatus
from app.exceptions import TradingPlatformException
from app.config import Config


@orders_bp.route('/orders', methods=['POST'])
def place_order():
    """
    Place a new order.
    
    Request Body:
        {
            "symbol": "AAPL",           // Required: Trading symbol
            "orderType": "BUY",         // Required: BUY or SELL
            "orderStyle": "MARKET",     // Required: MARKET or LIMIT
            "quantity": 10,             // Required: Must be > 0
            "price": 150.50             // Optional: Required for LIMIT orders
        }
        
    Returns:
        201: Order created successfully
        400: Validation error
        
    Example:
        POST /api/v1/orders
        {
            "symbol": "AAPL",
            "orderType": "BUY",
            "orderStyle": "MARKET",
            "quantity": 10
        }
        
    Response:
        {
            "order": {
                "id": 1,
                "symbol": "AAPL",
                "orderType": "BUY",
                "orderStyle": "MARKET",
                "quantity": 10,
                "status": "EXECUTED",
                ...
            },
            "trade": {
                "id": 1,
                "executedPrice": 150.25,
                "totalValue": 1502.50,
                ...
            },
            "message": "Order placed and executed successfully"
        }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        required_fields = ['symbol', 'orderType', 'orderStyle', 'quantity']
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Parse order parameters
        symbol = data.get('symbol', '').upper()
        order_type = OrderType[data.get('orderType').upper()]
        order_style = OrderStyle[data.get('orderStyle').upper()]
        quantity = int(data.get('quantity'))
        price = float(data.get('price')) if data.get('price') else None
        
        # Use default user (in real system, get from authentication)
        user_id = Config.DEFAULT_USER_ID
        
        # Create order
        order = OrderService.create_order(
            user_id=user_id,
            symbol=symbol,
            order_type=order_type,
            order_style=order_style,
            quantity=quantity,
            price=price
        )
        
        # Auto-execute market orders
        trade = None
        if order_style == OrderStyle.MARKET and Config.AUTO_EXECUTE_MARKET_ORDERS:
            trade = OrderExecutionEngine.execute_market_order(order)
        
        response = {
            'order': order.to_dict(),
            'message': 'Order placed successfully'
        }
        
        if trade:
            response['trade'] = trade.to_dict()
            response['message'] = 'Order placed and executed successfully'
        
        return jsonify(response), 201
        
    except TradingPlatformException as e:
        return jsonify(e.to_dict()), e.status_code
    except ValueError as e:
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get order status by ID.
    
    Path Parameters:
        order_id: Order ID
        
    Returns:
        200: Order details
        404: Order not found
        
    Example:
        GET /api/v1/orders/1
        
    Response:
        {
            "id": 1,
            "symbol": "AAPL",
            "orderType": "BUY",
            "status": "EXECUTED",
            ...
        }
    """
    try:
        order = OrderService.get_order_by_id(order_id)
        return jsonify(order.to_dict()), 200
    except TradingPlatformException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    """
    Get all orders for the user.
    
    Query Parameters:
        status: Optional order status filter (NEW, PLACED, EXECUTED, CANCELLED)
        
    Returns:
        200: List of orders
        
    Example:
        GET /api/v1/orders?status=EXECUTED
        
    Response:
        {
            "orders": [...],
            "count": 5
        }
    """
    try:
        user_id = Config.DEFAULT_USER_ID
        status_param = request.args.get('status')
        
        status = None
        if status_param:
            status = OrderStatus[status_param.upper()]
        
        orders = OrderService.get_user_orders(user_id, status)
        
        return jsonify({
            'orders': [order.to_dict() for order in orders],
            'count': len(orders)
        }), 200
    except ValueError as e:
        return jsonify({'error': f'Invalid status: {status_param}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """
    Cancel an order.
    
    Path Parameters:
        order_id: Order ID
        
    Returns:
        200: Order cancelled
        400: Cannot cancel (already executed/cancelled)
        404: Order not found
        
    Example:
        POST /api/v1/orders/1/cancel
    """
    try:
        order = OrderService.cancel_order(order_id)
        return jsonify({
            'order': order.to_dict(),
            'message': 'Order cancelled successfully'
        }), 200
    except TradingPlatformException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500