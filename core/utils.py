"""
Utility functions for DayTrade Analyzer Web.

This module provides helper functions that can be used across the project.
Place this file in the 'core' app so that other modules can import it as:
    from core.utils import get_local_data
"""

import os
import pandas as pd
from django.conf import settings
from datetime import datetime

def get_local_data(ticker, date=None):
    """
    Retrieve local stock data for the given ticker.

    Parameters:
      ticker (str): The stock ticker symbol.
      date (str, optional): A date string in "YYYY-MM-DD" format.
                            If provided, only data for that date is returned.
                            If not provided, all available data is returned.

    Returns:
      pandas.DataFrame: A DataFrame containing the local stock data with the index as datetime.

    Raises:
      Exception: If the data cannot be retrieved.
    """
    storage_method = settings.CONFIG.get('storage_method', 'csv')

    if storage_method == 'csv':
        # Construct the CSV file path
        csv_dir = settings.CONFIG.get("csv_data_dir", "csv_data")
        csv_path = os.path.join(settings.BASE_DIR, csv_dir, f"{ticker}.csv")
        try:
            local_data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")
    elif storage_method == 'postgres':
        try:
            from core.models import StockData
            # Query the StockData model for records with the given ticker
            qs = StockData.objects.filter(ticker=ticker).order_by("date")
            # Convert the QuerySet to a DataFrame
            local_data = pd.DataFrame(list(qs.values("date", "open", "high", "low", "close", "volume")))
            # Convert the 'date' column to datetime and set it as index
            local_data["date"] = pd.to_datetime(local_data["date"])
            local_data.set_index("date", inplace=True)
        except Exception as e:
            raise Exception(f"Error retrieving data from PostgreSQL: {e}")
    else:
        raise Exception("Invalid storage_method in config.")

    # Ensure the index is in datetime format.
    local_data.index = pd.to_datetime(local_data.index)

    # If a specific date is provided, filter the data to include only that day.
    if date is not None:
        try:
            # Convert the date string to a date object.
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
            # Filter local_data: compare the date portion of the index
            local_data = local_data[local_data.index.date == target_date]
        except Exception as e:
            raise Exception(f"Error processing the date parameter: {e}")

    return local_data
