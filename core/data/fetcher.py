"""
Module to fetch stock data using yfinance.
"""
import yfinance as yf
import time
import pytz

def fetch_stock_data(ticker, period="7d", interval="1m", retries=3, delay=5):
    """
    Fetch stock data(including pre-market and post-market) using yfinance with a retry mechanism.

    Parameters:
      ticker (str): The stock ticker symbol.
      period (str): The period of data to fetch (default "7d").
      interval (str): The data interval (default "1m").
      retries (int): The number of times to retry fetching data if it fails (default 3).
      delay (int): The delay in seconds between retries (default 5 seconds).

    Returns:
      DataFrame: The fetched stock data if successful.

    Raises:
      Exception: If the data cannot be fetched after the given number of retries.
    """
    for attempt in range(retries):
        try:
            # Attempt to download data, including pre-market and after-hours data
            ticker = yf.Ticker(ticker)
            data = ticker.history(period=period, interval=interval, prepost=True)
            # If data is successfully fetched and is not empty, return it
            if not data.empty:
                data.index = data.index.tz_convert('US/Eastern')
                # Remove timezone info if present
                if data.index.tz is not None:
                    data.index = data.index.tz_localize(None)
                return data[['Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
        # Wait for a specified delay before retrying
        time.sleep(delay)
    # If all attempts fail, raise an exception
    raise Exception("Failed to fetch data after multiple attempts.")