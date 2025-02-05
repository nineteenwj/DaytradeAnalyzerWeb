"""
Module to fetch stock data using yfinance.
"""
import yfinance as yf


def fetch_stock_data(ticker, period="7d", interval="1m"):
    """
    Fetch historical stock data for the given ticker.

    Parameters:
      ticker (str): The stock ticker symbol.
      period (str): The period to fetch data for (default "7d").
      interval (str): The data interval (default "1m").

    Returns:
      pandas.DataFrame: The fetched stock data.

    Raises:
      Exception: If no data is fetched.
    """
    data = yf.download(ticker, period=period, interval=interval)
    if data.empty:
        raise Exception("No data fetched; check ticker or network connection.")
    return data
