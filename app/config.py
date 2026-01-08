# File: app/config.py
"""
Configuration settings for the Trading Platform application.
Contains database, API, and environment-specific settings.
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Database settings - Using SQLite (in-memory for development)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///trading_platform.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Log all SQL queries (disable in production)
    
    # API settings
    API_TITLE = 'Trading Platform API'
    API_VERSION = 'v1'
    BASE_API_PREFIX = '/api/v1'
    
    # Pagination
    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE = 100
    
    # Mock user for authentication (simplified)
    DEFAULT_USER_ID = 'user_123'
    
    # Order execution settings
    AUTO_EXECUTE_MARKET_ORDERS = True
    EXECUTION_DELAY_SECONDS = 0  # Immediate execution
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///trading_dev.db'


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    # In production, use PostgreSQL or MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///trading_prod.db'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}