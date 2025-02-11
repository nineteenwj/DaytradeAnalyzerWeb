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

'''
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


def get_stock_list():
    """
    Retrieve a list of stocks that have local data stored.

    For each stock, this function returns a dictionary with:
      - 'ticker': the stock ticker (extracted from CSV filename or from the database)
      - 'start_date': the earliest date in the stored data (as a string, e.g., "YYYY-MM-DD")
      - 'end_date': the latest date in the stored data (as a string)

    Returns:
      List[dict]: A list of dictionaries, one for each stock.
    """
    stock_list = []
    storage_method = settings.CONFIG.get('storage_method', 'csv')

    if storage_method == 'csv':
        # Get the CSV directory from config
        csv_dir = os.path.join(settings.BASE_DIR, settings.CONFIG.get("csv_data_dir", "csv_data"))
        if os.path.exists(csv_dir):
            # Iterate over files ending with .csv in the directory
            for filename in os.listdir(csv_dir):
                if filename.endswith(".csv"):
                    ticker = filename[:-4]  # remove '.csv'
                    try:
                        data = pd.read_csv(os.path.join(csv_dir, filename), index_col=0, parse_dates=True)
                        data.index = pd.to_datetime(data.index)
                        if not data.empty:
                            start_date = data.index.min().strftime("%Y-%m-%d")
                            end_date = data.index.max().strftime("%Y-%m-%d")
                            stock_list.append({
                                "ticker": ticker,
                                "start_date": start_date,
                                "end_date": end_date
                            })
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")
    elif storage_method == 'postgres':
        try:
            from core.models import StockData
            # Query distinct tickers
            tickers = StockData.objects.values_list('ticker', flat=True).distinct()
            for ticker in tickers:
                qs = StockData.objects.filter(ticker=ticker).order_by("date")
                if qs.exists():
                    start_date = qs.first().date.strftime("%Y-%m-%d")
                    end_date = qs.last().date.strftime("%Y-%m-%d")
                    stock_list.append({
                        "ticker": ticker,
                        "start_date": start_date,
                        "end_date": end_date
                    })
        except Exception as e:
            print(f"Error retrieving stocks from PostgreSQL: {e}")
    return stock_list
'''


def get_local_data(ticker, date=None, market=None):
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
            if market != None:
                # 过滤 market 列为 'intraday' 的数据
                local_data = local_data[local_data['Market'] == market]
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


def get_all_stock_list():
    """
    Retrieve a list of stocks that have local data stored.

    For each stock, this function returns a dictionary with:
      - 'ticker': the stock ticker (extracted from CSV filename or from the database)
      - 'start_date': the earliest date in the stored data (as a string, e.g., "YYYY-MM-DD")
      - 'end_date': the latest date in the stored data (as a string)

    Returns:
      List[dict]: A list of dictionaries, one for each stock.
    """
    stock_list = []
    storage_method = settings.CONFIG.get('storage_method', 'csv')

    if storage_method == 'csv':
        # Get the CSV directory from config
        csv_dir = os.path.join(settings.BASE_DIR, settings.CONFIG.get("csv_data_dir", "csv_data"))
        if os.path.exists(csv_dir):
            # Iterate over files ending with .csv in the directory
            for filename in os.listdir(csv_dir):
                if filename.endswith(".csv"):
                    ticker = filename[:-4]  # remove '.csv'
                    try:
                        data = pd.read_csv(os.path.join(csv_dir, filename), index_col=0, parse_dates=True)
                        data.index = pd.to_datetime(data.index)
                        if not data.empty:
                            start_date = data.index.min().strftime("%Y-%m-%d")
                            end_date = data.index.max().strftime("%Y-%m-%d")
                            stock_list.append({
                                "ticker": ticker,
                                "stock_name": ticker,
                                "start_date": start_date,
                                "end_date": end_date
                            })
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")
    elif storage_method == 'postgres':
        try:
            from core.models import StockData
            # Query distinct tickers
            tickers = StockData.objects.values_list('ticker', flat=True).distinct()
            for ticker in tickers:
                qs = StockData.objects.filter(ticker=ticker).order_by("date")
                if qs.exists():
                    start_date = qs.first().date.strftime("%Y-%m-%d")
                    end_date = qs.last().date.strftime("%Y-%m-%d")
                    stock_list.append({
                        "ticker": ticker,
                        "stock_name": ticker,
                        "start_date": start_date,
                        "end_date": end_date
                    })
        except Exception as e:
            print(f"Error retrieving stocks from PostgreSQL: {e}")
    return stock_list


def query_local_stock_data(ticker, start_date, end_date, interval='1d'):
    """
    Fetches local stock data from CSV or PostgreSQL based on the ticker, start_date,
    end_date, and interval provided. The function supports intervals like '1d' and '1m'.

    Args:
      ticker (str): The stock ticker symbol (e.g., 'AAPL').
      start_date (str): The start date in the format 'YYYY-MM-DD'.
      end_date (str): The end date in the format 'YYYY-MM-DD'.
      interval (str): The data interval. Possible values are '1d', '1m', etc.

    Returns:
      list: A list of dictionaries with keys ['date', 'open', 'close', 'high', 'low', 'volume'].
    """

    # Determine the storage method (CSV or PostgreSQL)
    storage_method = settings.CONFIG.get("storage_method", "csv")

    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    if interval == '1d':
        # For "1d" interval, process minute-level data to calculate daily open, close, high, low, volume
        stock_data = []
        if storage_method == "csv":
            # Load CSV file if data is stored in CSV format
            csv_dir = os.path.join(settings.BASE_DIR, settings.CONFIG.get("csv_data_dir", "csv_data"))
            csv_path = os.path.join(csv_dir, f"{ticker}.csv")
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
                # set end_date to be next day, make sure it works when start_date = end_date
                end_date = end_date + pd.Timedelta(days=1)
                df = df[(df.index >= start_date) & (df.index < end_date)]
                if df.empty:
                    return []
                # Group by day and calculate Open, Close, High, Low, and Volume
                daily_data = df.groupby('Market').resample('D').agg({
                    'Open': 'first',  # First minute's open
                    'Close': 'last',  # Last minute's close
                    'High': 'max',  # Highest price
                    'Low': 'min',  # Lowest price
                    'Volume': 'sum'  # Sum of volumes
                })

                # 重新调整索引，将 Market 和 Date 重置为列
                daily_data = daily_data.reset_index()

                # 获取所有独特的日期
                unique_dates = daily_data['Datetime'].unique()

                for date in unique_dates:
                    # 过滤出该日期的数据
                    day_data = daily_data[daily_data['Datetime'] == date]
                    # 将 numpy.datetime64 转换为 pandas Timestamp 并格式化为字符串（去掉时分秒）
                    formatted_date = pd.to_datetime(date).strftime('%Y-%m-%d')

                    # 将同一天的不同市场数据合并成一个字典对象
                    day_dict = {
                        'date': formatted_date,
                        'markets': {}
                    }
                    # 遍历该天的不同 Market 数据
                    for _, row in day_data.iterrows():
                        market = row['Market']
                        day_dict['markets'][market] = {
                            'Open': round(row['Open'], 2),
                            'Close': round(row['Close'], 2),
                            'High': round(row['High'], 2),
                            'Low': round(row['Low'], 2),
                            'Volume': row['Volume']
                        }

                    # Convert the daily data to a list of dictionaries
                    stock_data.append(day_dict)

        elif storage_method == "postgres":
            # Use PostgreSQL if data is stored in PostgreSQL
            from core.models import StockData
            from django.db.models import Q
            stock_data_query = StockData.objects.filter(
                Q(ticker=ticker) & Q(date__range=[start_date, end_date])).order_by('date')

            # Convert query result to pandas DataFrame
            df = pd.DataFrame(list(stock_data_query.values('date', 'open', 'high', 'low', 'close', 'volume')))

            # Resample data by day and calculate daily statistics
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            daily_data = df.resample('D').agg({
                'open': 'first',  # First minute's open
                'close': 'last',  # Last minute's close
                'high': 'max',  # Highest price
                'low': 'min',  # Lowest price
                'volume': 'sum'  # Sum of volumes
            })

            # Convert to dictionary
            stock_data = daily_data.reset_index().to_dict(orient='records')

        else:
            raise ValueError("Invalid storage method specified.")

        return stock_data

    elif interval == '1m':
        # For "1m" interval, we return minute-level data as is
        if storage_method == "csv":
            # Load CSV data for minute-level data
            csv_dir = os.path.join(settings.BASE_DIR, settings.CONFIG.get("csv_data_dir", "csv_data"))
            csv_path = os.path.join(csv_dir, f"{ticker}.csv")
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
                df = df[(df.index >= start_date) & (df.index <= end_date)]
                if df.empty:
                    return []
                else:
                    return df.to_dict(orient='records')

        elif storage_method == "postgres":
            # For PostgreSQL, we query the minute-level data from StockData
            from core.models import StockData
            stock_data_query = StockData.objects.filter(
                Q(ticker=ticker) & Q(date__range=[start_date, end_date])).order_by('date')

            df = pd.DataFrame(list(stock_data_query.values('date', 'open', 'high', 'low', 'close', 'volume')))
            return df.to_dict(orient='records')

        else:
            raise ValueError("Invalid storage method specified.")

    else:
        raise ValueError(f"Unsupported interval: {interval}")

def get_previous_intraday_close(ticker, curent_date):
        """
        获取 current_date 对应日期的第一条记录的上一条记录的日期，表示上一个交易日的时间。
        如果第一条记录是整个数据集的第一条，则返回 None 或自定义消息。

        :param csv_path: 数据文件的路径
        :param start_date: 查询的起始日期，格式为 datetime 对象
        :return: 上一个交易日的日期或错误消息
        """
        # Load CSV file if data is stored in CSV format
        csv_dir = os.path.join(settings.BASE_DIR, settings.CONFIG.get("csv_data_dir", "csv_data"))
        csv_path = os.path.join(csv_dir, f"{ticker}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            if df.empty:
                return {}

        # 确保 start_date 是 datetime 对象
        current_date = pd.to_datetime(curent_date)

        # 获取 start_date 对应日期的所有数据
        day_data = df[df.index.date == current_date.date()]

        # 获取当天的第一条记录
        first_record = day_data.head(1)

        # 获取该记录的索引（时间戳）
        first_record_time = first_record.index[0]

        # 检查是否为整个数据集的第一条记录
        if first_record_time == df.index[0]:
            return {}  # 如果是第一条记录，则没有前一条记录

        # 获取第一条记录前一条记录的索引
        previous_record = df[df.index < first_record_time].iloc[-1:]

        # 获取前一条记录的日期
        previous_record_date = previous_record.index[0].date()

        target_time = pd.to_datetime(f"{previous_record_date} 16:00:00")

        if target_time in df.index:
            return df.loc[target_time].to_dict()
        else:
            print(f"指定的时间点 {target_time} 不在数据中")
            return {}

def add_stock(new_stock):
    stocks = get_all_stock_list()
    ret = False

    # Check if the new stock is already in the list (case-insensitive)
    existing_tickers = [stock["ticker"].upper() for stock in stocks]
    if new_stock in existing_tickers:
        msg = f"{new_stock} is already added."
    else:
        try:
            from core.data.fetcher import fetch_stock_data
            from core.data.storage import store_stock_data
            # Fetch and store stock data (1-minute data, 7 days)
            data = fetch_stock_data(new_stock, period="7d", interval="1m")
            store_stock_data(data, new_stock, settings.CONFIG)
            msg = f"{new_stock} has been added successfully."
            ret = True
        except Exception as e:
            msg = f"Error adding {new_stock}: {e}"
    return {'ret': ret, 'msg': msg}


def get_stock_info_by_date(ticker, date):

    stock_data = query_local_stock_data(ticker, date, date, '1d')
    if not stock_data:
        return {}

    tradedate = stock_data[0]['date']
    if 'pre-market' in stock_data[0]['markets']:
        pre_market_open = stock_data[0]['markets']['pre-market']['Open']
        pre_market_close = stock_data[0]['markets']['pre-market']['Close']
    else:
        pre_market_open = 0
        pre_market_close = 0
    # 盘前的涨跌幅是根据前一天盘中的收盘价为基准计算的
    last_day = get_previous_intraday_close(ticker, tradedate)
    if not last_day:
        last_day_close = pre_market_open
    else:
        last_day_close = last_day['Close']

    pre_market_change = ((pre_market_close - last_day_close) / last_day_close) * 100
    intraday_open = stock_data[0]['markets']['intraday']['Open']
    intraday_close = stock_data[0]['markets']['intraday']['Close']
    intraday_change = ((intraday_close - intraday_open) / intraday_open) * 100

    return {'pre_market_open': pre_market_open,
            'pre_market_close': pre_market_close,
            'pre_market_change': pre_market_change,
            'intraday_open': intraday_open,
            'intraday_close': intraday_close,
            'intraday_change:': intraday_change}