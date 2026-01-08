\# Trading Platform SDK



A comprehensive REST API and Python SDK for a simplified trading platform, similar to online stock broking applications like Robinhood or Zerodha.



\## 📋 Table of Contents



\- \[Features](#features)

\- \[Technology Stack](#technology-stack)

\- \[Installation](#installation)

\- \[Quick Start](#quick-start)

\- \[API Documentation](#api-documentation)

\- \[SDK Usage](#sdk-usage)

\- \[Project Structure](#project-structure)

\- \[Testing](#testing)

\- \[Contributing](#contributing)



\## ✨ Features



\### Core Features

\- ✅ View tradable financial instruments (stocks, options, futures)

\- ✅ Place BUY/SELL orders (MARKET and LIMIT)

\- ✅ Real-time order status tracking

\- ✅ View executed trades history

\- ✅ Portfolio management with P/L tracking

\- ✅ Automatic order execution engine

\- ✅ Comprehensive error handling



\### Technical Features

\- ✅ RESTful API design

\- ✅ Python SDK wrapper for easy integration

\- ✅ SQLite database (easy migration to PostgreSQL/MySQL)

\- ✅ Input validation and business logic



\## 🛠️ Technology Stack



\- \*\*Backend\*\*: Python 3.11+

\- \*\*Framework\*\*: Flask 3.0

\- \*\*ORM\*\*: SQLAlchemy

\- \*\*Database\*\*: SQLite (development) / PostgreSQL (production ready)

\- \*\*Testing\*\*: pytest

\- \*\*API Client\*\*: requests



\## 📦 Installation



\### Prerequisites

\- Python 3.11 or higher

\- pip (Python package manager)

\- Git



\### Step 1: Clone Repository

```bash

git clone https://github.com/YOUR-USERNAME/trading-platform.git

cd trading-platform

```



\### Step 2: Create Virtual Environment

```bash

\# Windows

python -m venv venv

venv\\Scripts\\activate



\# macOS/Linux

python3 -m venv venv

source venv/bin/activate

```



\### Step 3: Install Dependencies

```bash

pip install -r requirements.txt

```



\### Step 4: Run Application

```bash

python run.py

```



The application will start on `http://localhost:5000`



\## 🚀 Quick Start



\### Using the API Directly

```bash

\# Get all instruments

curl http://localhost:5000/api/v1/instruments



\# Place a buy order

curl -X POST http://localhost:5000/api/v1/orders \\

&nbsp; -H "Content-Type: application/json" \\

&nbsp; -d "{\\"symbol\\":\\"AAPL\\",\\"orderType\\":\\"BUY\\",\\"orderStyle\\":\\"MARKET\\",\\"quantity\\":10}"



\# Get portfolio

curl http://localhost:5000/api/v1/portfolio

```



\### Using the Python SDK

```python

from sdk.trading\_sdk import TradingSDK



\# Initialize SDK

sdk = TradingSDK(base\_url='http://localhost:5000')



\# Get instruments

instruments = sdk.get\_instruments()

print(f"Available instruments: {len(instruments)}")



\# Place a market buy order

result = sdk.place\_buy\_order('AAPL', 10)

print(f"Order placed: {result\['order']\['status']}")



\# View portfolio

portfolio = sdk.get\_portfolio()

print(f"Portfolio value: ${portfolio\['totalCurrentValue']:.2f}")



sdk.close()

```



\## 📚 API Documentation



\### Base URL

```

http://localhost:5000/api/v1

```



\### Endpoints



\#### 1. Instruments



\*\*GET /instruments\*\*

Get all tradable instruments.

```bash

curl http://localhost:5000/api/v1/instruments

```



Response:

```json

{

&nbsp; "instruments": \[

&nbsp;   {

&nbsp;     "id": 1,

&nbsp;     "symbol": "AAPL",

&nbsp;     "name": "Apple Inc.",

&nbsp;     "exchange": "NASDAQ",

&nbsp;     "instrumentType": "EQUITY",

&nbsp;     "lastTradedPrice": 175.50,

&nbsp;     "isActive": true

&nbsp;   }

&nbsp; ],

&nbsp; "count": 10

}

```



\*\*GET /instruments/{symbol}\*\*

Get specific instrument.

```bash

curl http://localhost:5000/api/v1/instruments/AAPL

```



\#### 2. Orders



\*\*POST /orders\*\*

Place a new order.



Request Body:

```json

{

&nbsp; "symbol": "AAPL",

&nbsp; "orderType": "BUY",

&nbsp; "orderStyle": "MARKET",

&nbsp; "quantity": 10,

&nbsp; "price": 150.00  // Optional, required for LIMIT orders

}

```

```bash

curl -X POST http://localhost:5000/api/v1/orders \\

&nbsp; -H "Content-Type: application/json" \\

&nbsp; -d "{\\"symbol\\":\\"AAPL\\",\\"orderType\\":\\"BUY\\",\\"orderStyle\\":\\"MARKET\\",\\"quantity\\":10}"

```



Response:

```json

{

&nbsp; "order": {

&nbsp;   "id": 1,

&nbsp;   "symbol": "AAPL",

&nbsp;   "orderType": "BUY",

&nbsp;   "orderStyle": "MARKET",

&nbsp;   "quantity": 10,

&nbsp;   "status": "EXECUTED",

&nbsp;   "createdAt": "2024-01-15T10:30:00"

&nbsp; },

&nbsp; "trade": {

&nbsp;   "id": 1,

&nbsp;   "executedPrice": 175.50,

&nbsp;   "totalValue": 1755.00,

&nbsp;   "executedAt": "2024-01-15T10:30:01"

&nbsp; },

&nbsp; "message": "Order placed and executed successfully"

}

```



\*\*GET /orders/{orderId}\*\*

Get order status.

```bash

curl http://localhost:5000/api/v1/orders/1

```



\*\*GET /orders?status={status}\*\*

Get all orders (optionally filtered by status).

```bash

curl http://localhost:5000/api/v1/orders?status=EXECUTED

```



\*\*POST /orders/{orderId}/cancel\*\*

Cancel an order.

```bash

curl -X POST http://localhost:5000/api/v1/orders/1/cancel

```



\#### 3. Trades



\*\*GET /trades?symbol={symbol}\*\*

Get executed trades.

```bash

curl http://localhost:5000/api/v1/trades?symbol=AAPL

```



Response:

```json

{

&nbsp; "trades": \[

&nbsp;   {

&nbsp;     "id": 1,

&nbsp;     "orderId": 1,

&nbsp;     "symbol": "AAPL",

&nbsp;     "tradeType": "BUY",

&nbsp;     "quantity": 10,

&nbsp;     "executedPrice": 175.50,

&nbsp;     "totalValue": 1755.00,

&nbsp;     "executedAt": "2024-01-15T10:30:01"

&nbsp;   }

&nbsp; ],

&nbsp; "count": 1

}

```



\#### 4. Portfolio



\*\*GET /portfolio\*\*

Get user portfolio.

```bash

curl http://localhost:5000/api/v1/portfolio

```



Response:

```json

{

&nbsp; "holdings": \[

&nbsp;   {

&nbsp;     "symbol": "AAPL",

&nbsp;     "quantity": 10,

&nbsp;     "averagePrice": 175.50,

&nbsp;     "totalInvested": 1755.00,

&nbsp;     "currentValue": 1760.00,

&nbsp;     "profitLoss": 5.00,

&nbsp;     "profitLossPercentage": 0.28

&nbsp;   }

&nbsp; ],

&nbsp; "totalInvested": 1755.00,

&nbsp; "totalCurrentValue": 1760.00,

&nbsp; "totalProfitLoss": 5.00,

&nbsp; "count": 1

}

```



\## 🐍 SDK Usage



\### Installation



The SDK is included in the project. Just import it:

```python

from sdk.trading\_sdk import TradingSDK, TradingSDKException

```



\### Basic Usage

```python

from sdk.trading\_sdk import TradingSDK



\# Initialize

sdk = TradingSDK(base\_url='http://localhost:5000')



try:

&nbsp;   # Get all instruments

&nbsp;   instruments = sdk.get\_instruments()

&nbsp;   

&nbsp;   # Get specific instrument

&nbsp;   aapl = sdk.get\_instrument('AAPL')

&nbsp;   

&nbsp;   # Place market buy order

&nbsp;   result = sdk.place\_buy\_order('AAPL', 10)

&nbsp;   

&nbsp;   # Place limit buy order

&nbsp;   result = sdk.place\_buy\_order('AAPL', 5, price=150.00)

&nbsp;   

&nbsp;   # Place sell order

&nbsp;   result = sdk.place\_sell\_order('AAPL', 5)

&nbsp;   

&nbsp;   # Get order status

&nbsp;   order = sdk.get\_order(order\_id=1)

&nbsp;   

&nbsp;   # Get all orders

&nbsp;   orders = sdk.get\_orders()

&nbsp;   

&nbsp;   # Get orders by status

&nbsp;   executed\_orders = sdk.get\_orders(status='EXECUTED')

&nbsp;   

&nbsp;   # Cancel order

&nbsp;   result = sdk.cancel\_order(order\_id=1)

&nbsp;   

&nbsp;   # Get trades

&nbsp;   trades = sdk.get\_trades()

&nbsp;   

&nbsp;   # Get trades for specific symbol

&nbsp;   aapl\_trades = sdk.get\_trades(symbol='AAPL')

&nbsp;   

&nbsp;   # Get portfolio

&nbsp;   portfolio = sdk.get\_portfolio()

&nbsp;   

&nbsp;   # Get specific holding

&nbsp;   aapl\_holding = sdk.get\_holding('AAPL')



except TradingSDKException as e:

&nbsp;   print(f"Error: {e.message}")

&nbsp;   print(f"Status Code: {e.status\_code}")



finally:

&nbsp;   sdk.close()

```



\### Using Context Manager

```python

from sdk.trading\_sdk import TradingSDK



with TradingSDK('http://localhost:5000') as sdk:

&nbsp;   instruments = sdk.get\_instruments()

&nbsp;   # SDK automatically closes

```



\### Error Handling

```python

from sdk.trading\_sdk import TradingSDK, TradingSDKException



sdk = TradingSDK('http://localhost:5000')



try:

&nbsp;   # This will raise an exception if invalid

&nbsp;   result = sdk.place\_buy\_order('INVALID', 10)

&nbsp;   

except TradingSDKException as e:

&nbsp;   print(f"Error: {e.message}")

&nbsp;   # Error: Instrument 'INVALID' not found or not tradable

&nbsp;   

&nbsp;   print(f"Status: {e.status\_code}")

&nbsp;   # Status: 404

&nbsp;   

&nbsp;   print(f"Details: {e.response}")

&nbsp;   # Details: {'error': '...', 'symbol': 'INVALID'}

```



\## 📁 Project Structure

```

trading-platform/

├── app/

│   ├── \_\_init\_\_.py              # Application factory

│   ├── config.py                # Configuration settings

│   ├── models/                  # Database models

│   │   ├── \_\_init\_\_.py

│   │   ├── instrument.py

│   │   ├── order.py

│   │   ├── trade.py

│   │   └── portfolio.py

│   ├── routes/                  # API endpoints

│   │   ├── \_\_init\_\_.py

│   │   ├── instruments.py

│   │   ├── orders.py

│   │   ├── trades.py

│   │   └── portfolio.py

│   ├── services/                # Business logic

│   │   ├── \_\_init\_\_.py

│   │   ├── instrument\_service.py

│   │   ├── order\_service.py

│   │   ├── trade\_service.py

│   │   ├── portfolio\_service.py

│   │   └── execution\_engine.py

│   └── exceptions/              # Custom exceptions

│       ├── \_\_init\_\_.py

│       └── custom\_exceptions.py

├── sdk/                         # Python SDK

│   ├── \_\_init\_\_.py

│   └── trading\_sdk.py

├── examples/                    # Usage examples

│   └── (example scripts)

├── requirements.txt             # Python dependencies

├── run.py                       # Application entry point

├── .gitignore                   # Git ignore file

└── README.md                    # This file

```



\## 🧪 Testing



\### Run Tests

```bash

\# Run all tests

pytest



\# Run with coverage

pytest --cov=app --cov=sdk



\# Run specific test file

pytest tests/test\_orders.py



\# Run with verbose output

pytest -v

```



\### Manual Testing

```bash

\# Test with the included script

python test\_sdk\_quick.py

```



\## 🎯 Design Decisions



\### Architecture

\- \*\*Layered Architecture\*\*: Clear separation between API, Service, and Data layers

\- \*\*Repository Pattern\*\*: Centralized data access

\- \*\*Service Layer\*\*: Business logic separated from controllers



\### Database

\- \*\*SQLite\*\*: Easy setup for development

\- \*\*SQLAlchemy ORM\*\*: Database-agnostic, easy migration to PostgreSQL/MySQL



\### Order Execution

\- \*\*Automatic execution\*\* for MARKET orders

\- \*\*Simplified execution\*\* for LIMIT orders (immediate at limit price)

\- Real-world systems would have complex matching engines



\### Error Handling

\- \*\*Custom exception hierarchy\*\* for different error types

\- \*\*Meaningful error messages\*\* with appropriate HTTP status codes

\- \*\*Validation\*\* at multiple layers






\## 📄 License



This project is created for educational purposes.



\## 👤 Author



\*\*ROOPSA\*\*

\- GitHub: \[@roopsa2004(https://github.com/roopsa2004)

\- LinkedIn: \(https://www.linkedin.com/in/roopsa-bhattacharya-04450530b/)



\## 🙏 Acknowledgments



\- Built as part of a trading platform assessment

\- Inspired by real-world trading platforms like Robinhood and Zerodha



---



\*\*Note\*\*: This is a simplified trading platform for demonstration purposes. It does not connect to real markets or handle real money.

