# File: run.py
"""
Main entry point for running the application.
Usage: python run.py
"""
import os
from app import create_app

# Create application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Trading Platform API Starting...")
    print("="*60)
    print(f"📍 Server running at: http://localhost:5000")
    print(f"📍 Health check: http://localhost:5000/health")
    print(f"📍 API docs: http://localhost:5000/api-docs/")
    print(f"📍 Instruments: http://localhost:5000/api/v1/instruments")
    print("="*60 + "\n")
    
    # Run development server on port 5000
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )