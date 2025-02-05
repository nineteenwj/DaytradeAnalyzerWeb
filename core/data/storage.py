"""
Module to store stock data.
Depending on the configuration, data is stored either in CSV files or in PostgreSQL via Django models.
"""
import os
import pandas as pd
from core.models import StockData


def store_stock_data(data, ticker, config):
    """
    Store the fetched stock data.

    Parameters:
      data (DataFrame): The stock data.
      ticker (str): The stock ticker symbol.
      config (dict): The configuration dictionary loaded from config.yaml.

    Raises:
      Exception: If storage fails.
    """
    method = config.get('storage_method', 'csv')
    if method == 'csv':
        # CSV storage
        csv_dir = config.get('csv_data_dir', 'csv_data')
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        csv_path = os.path.join(csv_dir, f"{ticker}.csv")
        try:
            data.to_csv(csv_path, index=True)
        except Exception as e:
            raise Exception(f"Error writing CSV: {e}")
    elif method == 'postgres':
        # PostgreSQL storage using the StockData model
        try:
            for index, row in data.iterrows():
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
                        'volume': int(row['Volume'])
                    }
                )
        except Exception as e:
            raise Exception(f"Error storing in PostgreSQL: {e}")
    else:
        raise Exception("Invalid storage_method in config.")
