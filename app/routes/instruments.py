# File: app/routes/instruments.py
"""
Instrument API endpoints.
Handles requests for viewing available instruments.
"""
from flask import jsonify, request
from app.routes import instruments_bp
from app.services.instrument_service import InstrumentService


@instruments_bp.route('/instruments', methods=['GET'])
def get_instruments():
    """
    Get all tradable instruments.
    
    Query Parameters:
        active_only: boolean (default: true) - Return only active instruments
        
    Returns:
        200: List of instruments
        
    Example:
        GET /api/v1/instruments
        
    Response:
        {
            "instruments": [
                {
                    "id": 1,
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "exchange": "NASDAQ",
                    "instrumentType": "EQUITY",
                    "lastTradedPrice": 150.25,
                    "isActive": true
                }
            ],
            "count": 1
        }
    """
    try:
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        instruments = InstrumentService.get_all_instruments(active_only)
        
        return jsonify({
            'instruments': [inst.to_dict() for inst in instruments],
            'count': len(instruments)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@instruments_bp.route('/instruments/<string:symbol>', methods=['GET'])
def get_instrument(symbol):
    """
    Get specific instrument by symbol.
    
    Path Parameters:
        symbol: Trading symbol (e.g., AAPL)
        
    Returns:
        200: Instrument details
        404: Instrument not found
        
    Example:
        GET /api/v1/instruments/AAPL
    """
    try:
        instrument = InstrumentService.get_instrument_by_symbol(symbol)
        return jsonify(instrument.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404