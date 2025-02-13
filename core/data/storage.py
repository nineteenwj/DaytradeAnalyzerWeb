"""
Module to store stock data.
Depending on the configuration, data is stored either in CSV files or in PostgreSQL via Django models.
"""
import os
import pandas as pd
from core.models import StockData
from datetime import time as dtime


def store_stock_data(data, ticker, config):
    """
    Store the fetched stock data after adjusting it.

    If storage_method is "csv", the function reads any existing CSV file for the ticker.
    It then determines which dates are not already stored and appends only new data.

    If storage_method is "postgres", it uses get_or_create to avoid duplicate entries.

    Parameters:
      data (DataFrame): The stock data.
      ticker (str): The stock ticker symbol.
      config (dict): The configuration dictionary loaded from config.yaml.

    Raises:
      Exception: If storage fails.
    """
    # Adjust the data (remove timezone info and add MarketSession column)
    adjusted_data = adjust_data(data)

    method = config.get('storage_method', 'csv')
    if method == 'csv':
        # CSV storage
        csv_path = os.path.join(config.get('csv_data_dir', 'csv_data'),f"{ticker}.csv")
        # If the CSV file exists, read it and then append only new data.
        if os.path.exists(csv_path):
            try:
                existing_data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            except Exception as e:
                raise Exception(f"Error reading existing CSV file: {e}")

            # Determine which dates are already stored.
            # We'll compare date strings (YYYY-MM-DD).
            existing_dates = set(existing_data.index.strftime("%Y-%m-%d"))

            # Filter adjusted_data to include only rows with dates not already stored.
            new_data = adjusted_data[~adjusted_data.index.strftime("%Y-%m-%d").isin(existing_dates)]

            if new_data.empty:
                # No new data to append; do nothing.
                return
            else:
                # Append new data to the CSV file.
                try:
                    # Append without writing header.
                    new_data.to_csv(csv_path, mode='a', header=False)
                except Exception as e:
                    raise Exception(f"Error appending new data to CSV: {e}")
        else:
            # CSV file does not exist; create a new one.
            try:
                adjusted_data.to_csv(csv_path, index=True)
            except Exception as e:
                raise Exception(f"Error writing CSV: {e}")
    elif method == 'postgres':
        # PostgreSQL storage using the StockData model
        try:
            for index, row in adjust_data.iterrows():
                # Ensure index is datetime
                dt = index.to_pydatetime() if hasattr(index, 'to_pydatetime') else index

                StockData.objects.get_or_create(
                    ticker=ticker,
                    date=dt,
                    defaults={
                        'open': row['Open'],
                        'high': row['High'],
                        'low': row['Low'],
                        'close': row['Close'],
                        'volume': int(row['Volume']),
                        'market':row['Market']
                    }
                )
        except Exception as e:
            raise Exception(f"Error storing in PostgreSQL: {e}")
    else:
        raise Exception("Invalid storage_method in config.")


def adjust_data(data):
    """
    Adjust the fetched stock data before writing to storage.

    1. Remove any timezone information from the index.
    2. Add a new column "MarketSession" based on the time of day:
         - From 04:00:00 (inclusive) to 09:30:00 (exclusive): "pre-market"
         - From 09:30:00 (inclusive) to 16:00:00 (inclusive): "intraday"
         - From 16:01:00 (inclusive) to 19:59:59 (inclusive): "post-market"
         - Otherwise: "unknown"

    Parameters:
      data (DataFrame): The stock data fetched from yfinance.

    Returns:
      DataFrame: The adjusted DataFrame.
    """

    # Define a helper function to determine the market session based on time.
    def get_market_session(dt):
        t = dt.time()
        if dtime(4, 0, 0) <= t < dtime(9, 30, 0):
            return "pre-market"
        elif dtime(9, 30, 0) <= t <= dtime(16, 0, 0):
            return "intraday"
        elif dtime(16, 1, 0) <= t <= dtime(19, 59, 59):
            return "post-market"
        else:
            return "unknown"

    # Add a new column "MarketSession" by applying the helper function to the index.
    data["Market"] = data.index.map(get_market_session)
    return data
