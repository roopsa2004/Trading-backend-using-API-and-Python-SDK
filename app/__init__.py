# File: app/__init__.py
"""
Main application factory.
Creates and configures the Flask application.
"""
import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

# Initialize extensions
db = SQLAlchemy()


def create_app(config_name=None):
    """
    Application factory pattern.
    Creates and configures the Flask application.
    
    Args:
        config_name: Configuration to use (development/testing/production)
        
    Returns:
        Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Configure Swagger/OpenAPI documentation
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api-docs/"
    }
    
    swagger_template = {
        "info": {
            "title": "Trading Platform API",
            "description": "REST API for a simplified trading platform",
            "version": "1.0.0",
            "contact": {
                "name": "API Support"
            }
        },
        "schemes": ["http", "https"],
        "tags": [
            {"name": "Instruments", "description": "Tradable instruments operations"},
            {"name": "Orders", "description": "Order management"},
            {"name": "Trades", "description": "Executed trades"},
            {"name": "Portfolio", "description": "User portfolio holdings"}
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Register blueprints (API routes)
    from app.routes import instruments_bp, orders_bp, trades_bp, portfolio_bp
    
    api_prefix = app.config['BASE_API_PREFIX']
    app.register_blueprint(instruments_bp, url_prefix=api_prefix)
    app.register_blueprint(orders_bp, url_prefix=api_prefix)
    app.register_blueprint(trades_bp, url_prefix=api_prefix)
    app.register_blueprint(portfolio_bp, url_prefix=api_prefix)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create database tables and initialize data
    with app.app_context():
        db.create_all()
        initialize_sample_data()
    
    # Configure logging
    configure_logging(app)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'trading-platform'}), 200
    
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'service': 'Trading Platform API',
            'version': '1.0.0',
            'documentation': '/api-docs/',
            'endpoints': {
                'instruments': f'{api_prefix}/instruments',
                'orders': f'{api_prefix}/orders',
                'trades': f'{api_prefix}/trades',
                'portfolio': f'{api_prefix}/portfolio'
            }
        }), 200
    
    return app


def register_error_handlers(app):
    """Register global error handlers"""
    from app.exceptions import TradingPlatformException
    
    @app.errorhandler(TradingPlatformException)
    def handle_trading_exception(error):
        return jsonify(error.to_dict()), error.status_code
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({'error': 'Resource not found', 'status': 404}), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        return jsonify({'error': 'Internal server error', 'status': 500}), 500


def configure_logging(app):
    """Configure application logging"""
    logging.basicConfig(
        level=getattr(logging, app.config['LOG_LEVEL']),
        format=app.config['LOG_FORMAT']
    )


def initialize_sample_data():
    """Initialize database with sample instruments"""
    from app.models import Instrument, InstrumentType
    from decimal import Decimal
    
    # Check if data already exists
    if Instrument.query.count() > 0:
        return
    
    # Sample instruments
    instruments = [
        {
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'exchange': 'NASDAQ',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('175.50')
        },
        {
            'symbol': 'GOOGL',
            'name': 'Alphabet Inc.',
            'exchange': 'NASDAQ',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('140.25')
        },
        {
            'symbol': 'MSFT',
            'name': 'Microsoft Corporation',
            'exchange': 'NASDAQ',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('380.75')
        },
        {
            'symbol': 'TSLA',
            'name': 'Tesla, Inc.',
            'exchange': 'NASDAQ',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('245.30')
        },
        {
            'symbol': 'AMZN',
            'name': 'Amazon.com, Inc.',
            'exchange': 'NASDAQ',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('155.80')
        },
        {
            'symbol': 'NVDA',
            'name': 'NVIDIA Corporation',
            'exchange': 'NASDAQ',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('495.20')
        },
        {
            'symbol': 'META',
            'name': 'Meta Platforms, Inc.',
            'exchange': 'NASDAQ',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('350.10')
        },
        {
            'symbol': 'JPM',
            'name': 'JPMorgan Chase & Co.',
            'exchange': 'NYSE',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('158.90')
        },
        {
            'symbol': 'V',
            'name': 'Visa Inc.',
            'exchange': 'NYSE',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('245.60')
        },
        {
            'symbol': 'WMT',
            'name': 'Walmart Inc.',
            'exchange': 'NYSE',
            'instrument_type': InstrumentType.EQUITY,
            'last_traded_price': Decimal('165.40')
        }
    ]
    
    for inst_data in instruments:
        instrument = Instrument(**inst_data)
        db.session.add(instrument)
    
    db.session.commit()
    print(f"✓ Initialized {len(instruments)} sample instruments")