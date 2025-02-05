# DayTrade Analyzer Web

A Django web application for intraday trading analysis and simulation. This project uses Django as the backend and Material-Kit (free version) for the frontend. It supports fetching US stock data via yfinance, displaying candlestick charts with technical indicators, and simulating trades.

## Features

- **Data Retrieval:**  
  Fetch US stock data (1-minute interval for the last 7 days) via yfinance.
- **Data Presentation:**  
  Display candlestick charts and technical indicators.
- **Trading Simulation:**  
  Simulate trades for up to 5 dates by inputting Buy Price, Stop Loss (%), and Take Profit (%).
- **Flexible Data Storage:**  
  Store data either in CSV files or in a PostgreSQL database, as configured in `config.yaml`.
- **Bilingual Documentation:**  
  This project includes README files in both English and Chinese.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/daytrade-analyzer-web.git
   cd daytrade-analyzer-web
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Edit config.yaml to select the storage method ("csv" or "postgres") and set database parameters if needed.
5. If using PostgreSQL, update the DATABASES setting in daytradeanalyzerweb/settings.py accordingly.
6. Apply migrations:
   ```bash
   python manage.py migrate
7. Run the development server:
   ```bash
   python manage.py runserver
8. Open your browser at http://localhost:8000.

## Usage
- On the homepage, enter a stock ticker and select a date range.
- Click Get Stock Data to fetch and store data.
- The presentation panel will display a candlestick chart.
- The trading simulation panel (on the same page) allows you to simulate trades for 5 dates by selecting a date (from a drop-down) and entering trading parameters.
- Click Simulate All to run the simulation.

## Configuration
The configuration file config.yaml controls data storage:
- storage_method: "csv" or "postgres"
- csv_data_dir: Directory for CSV files.
- database: PostgreSQL connection parameters (if using "postgres").

## License
This project is licensed under the GNU General Public License v3.0.

