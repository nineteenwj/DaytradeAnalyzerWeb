"""
Module to fetch stock data using yfinance.
"""
import yfinance as yf
import time

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
                return data[['Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
        # Wait for a specified delay before retrying
        time.sleep(delay)
    # If all attempts fail, raise an exception
    raise Exception("Failed to fetch data after multiple attempts.")


# Fetch company information (market cap, PE ratio, dividend, etc.)
def fetch_company_info(ticker):
    """
    Fetch company information such as market cap, PE ratio, dividend yield, etc.
    :param ticker: Stock ticker symbol
    :return: Dictionary containing company information, or empty dictionary if data is unavailable
    """
    try:
        ticker_data = yf.Ticker(ticker)
        company_info = ticker_data.info

        # If the info dictionary is empty, return an empty dictionary
        if not company_info:
            return {}
        return company_info
    except Exception as e:
        print(f"Error fetching company info for {ticker}: {e}")
        return {}  # Return an empty dictionary in case of error


# Fetch financial statements (income statement, balance sheet, cash flow)
def fetch_financials(ticker):
    """
    Fetch financial statements including income statement, balance sheet, and cash flow statement.
    :param ticker: Stock ticker symbol
    :return: Dictionary containing financial statements, or empty dictionary if data is unavailable
    """
    try:
        ticker_data = yf.Ticker(ticker)
        financials = ticker_data.financials

        # If financials data is empty, return an empty dictionary
        if financials.empty:
            return {}

        # Convert financials DataFrame to dict if it's not empty
        return financials.to_dict()
    except Exception as e:
        print(f"Error fetching financials for {ticker}: {e}")
        return {}  # Return an empty dictionary in case of error


# Fetch dividend data
def fetch_dividends(ticker):
    """
    Fetch historical dividend data for the given ticker.
    :param ticker: Stock ticker symbol
    :return: List containing dividend data, or empty list if data is unavailable
    """
    try:
        ticker_data = yf.Ticker(ticker)
        dividends = ticker_data.dividends

        # If dividends data is empty, return an empty list
        if dividends.empty:
            return []

        # Convert Series to list and return
        return dividends.tolist()
    except Exception as e:
        print(f"Error fetching dividends for {ticker}: {e}")
        return []  # Return an empty list in case of error


# Fetch stock splits data
def fetch_splits(ticker):
    """
    Fetch stock split data for the given ticker.
    :param ticker: Stock ticker symbol
    :return: List containing stock split data, or empty list if data is unavailable
    """
    try:
        ticker_data = yf.Ticker(ticker)
        splits = ticker_data.splits

        # If splits data is empty, return an empty list
        if splits.empty:
            return []

        # Convert Series to list and return
        return splits.tolist()
    except Exception as e:
        print(f"Error fetching splits for {ticker}: {e}")
        return []  # Return an empty list in case of error


# Fetch analyst recommendations data
def fetch_analyst_recommendations(ticker):
    """
    Fetch analyst recommendations for the given ticker.
    :param ticker: Stock ticker symbol
    :return: List of analyst recommendations, or empty list if data is unavailable
    """
    try:
        ticker_data = yf.Ticker(ticker)
        recommendations = ticker_data.recommendations

        # If recommendations data is empty, return an empty list
        if recommendations.empty:
            return []

        # Convert recommendations DataFrame to list of dictionaries and return
        return recommendations.to_dict(orient='records')
    except Exception as e:
        print(f"Error fetching analyst recommendations for {ticker}: {e}")
        return []  # Return an empty list in case of error


# Fetch options data for the given ticker
def fetch_options(ticker):
    """
    Fetch options expiration dates for the given ticker.
    :param ticker: Stock ticker symbol
    :return: List of available options expiration dates, or empty list if data is unavailable
    """
    try:
        ticker_data = yf.Ticker(ticker)
        options_dates = ticker_data.options

        # If no options are available, return an empty list
        if not options_dates:
            return []
        return options_dates
    except Exception as e:
        print(f"Error fetching options for {ticker}: {e}")
        return []  # Return an empty list in case of error


# Main execution for testing purposes when this script is run directly
if __name__ == "__main__":
    # Choose a stock ticker symbol for testing
    ticker = "AAPL"  # Example: Apple Inc.

    print(f"Fetching historical data for {ticker}...")
    historical_data = fetch_stock_data(ticker, period="5d", interval="1d")
    print(historical_data)

    print(f"\nFetching company information for {ticker}...")
    company_info = fetch_company_info(ticker)
    print(company_info)

    print(f"\nFetching financials for {ticker}...")
    financials = fetch_financials(ticker)
    print(financials)

    print(f"\nFetching dividends for {ticker}...")
    dividends = fetch_dividends(ticker)
    print(dividends)

    print(f"\nFetching stock splits for {ticker}...")
    splits = fetch_splits(ticker)
    print(splits)

    print(f"\nFetching analyst recommendations for {ticker}...")
    recommendations = fetch_analyst_recommendations(ticker)
    print(recommendations)

    print(f"\nFetching options for {ticker}...")
    options_dates = fetch_options(ticker)
    print(options_dates)