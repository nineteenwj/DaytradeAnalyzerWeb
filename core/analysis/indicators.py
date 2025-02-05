"""
Module to calculate technical indicators.
Currently, a simple 5-period Simple Moving Average (SMA) is implemented.
"""
import pandas as pd


def add_technical_indicators(data):
    """
    Add technical indicators to the data.

    For example, add a 5-period SMA to the 'Close' prices.

    Parameters:
      data (DataFrame): The stock data.

    Returns:
      DataFrame: The data with additional indicator columns.
    """
    data['SMA_5'] = data['Close'].rolling(window=5).mean()
    return data
