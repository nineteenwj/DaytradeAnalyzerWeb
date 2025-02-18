"""
Module to store stock data.
Depending on the configuration, data is stored either in CSV files or in PostgreSQL via Django models.
"""
import os
import pandas as pd
from core.models import StockData, StockInfo, AnalystRecommendation
from datetime import time as dtime, datetime
from django.db import IntegrityError


def store_stock_data(ticker, data, config):
    """
    Store the fetched stock data after adjusting it.

    If storage_method is "csv", the function reads any existing CSV file for the ticker.
    It then determines which dates are not already stored and appends only new data.

    If storage_method is "postgres", it uses get_or_create to avoid duplicate entries.

    Parameters:
      ticker (str): The stock ticker symbol.
      data (DataFrame): The stock data.
      config (dict): The configuration dictionary loaded from config.yaml.

    Raises:
      Exception: If storage fails.
    """
    # Adjust the data (remove timezone info and add MarketSession column)
    adjusted_data = adjust_data(data)

    method = config.get('storage_method', 'csv')
    if method == 'csv':
        # Remove timezone info if present
        if adjusted_data.index.tz is not None:
            adjusted_data.index = adjusted_data.index.tz_localize(None)
        # CSV storage
        csv_path = os.path.join(config.get('csv_data_dir', 'csv_data'), f"{ticker}.csv")
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
        print('In store_stock_data postgres')
        # PostgreSQL storage using the StockData model
        try:
            for index, row in adjusted_data.iterrows():
                # Ensure index is datetime
                #dt = index.to_pydatetime() if hasattr(index, 'to_pydatetime') else index

                StockData.objects.get_or_create(
                    ticker=ticker,
                    date=index,
                    defaults={
                        'open': row['Open'],
                        'high': row['High'],
                        'low': row['Low'],
                        'close': row['Close'],
                        'volume': int(row['Volume']),
                        'market': row['Market']
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


def store_stock_info(ticker, info, config):
    """
    Fetch company information and save it either to a CSV file or PostgreSQL database.
    :param ticker_code: Stock ticker symbol (e.g., 'AAPL', 'GOOG')
    :param method: Optional storage method. If None, it reads from the config.
    """
    try:

        if not info:
            print(f"No data available for {ticker}.")
            return

        # Prepare data in a dictionary
        '''
        data = {
            "ticker": [ticker],
            "website": [info.get('website', '')],
            "industry": [info.get('industry', '')],
            "sector": [info.get('sector', '')],
            "long_business_summary": [info.get('longBusinessSummary', '')],
            "full_time_employees": [info.get('fullTimeEmployees', '')],
            "audit_risk": [info.get('auditRisk', '')],
            "board_risk": [info.get('boardRisk', '')],
            "compensation_risk": [info.get('compensationRisk', '')],
            "share_holder_rights_risk": [info.get('shareHolderRightsRisk', '')],
            "overall_risk": [info.get('overallRisk', '')],
            "dividend_rate": [info.get('dividendRate', '')],
            "dividend_yield": [info.get('dividendYield', '')],
            "ex_dividend_date": [info.get('exDividendDate', '')],
            "payout_ratio": [info.get('payoutRatio', '')],
            "five_year_avg_dividend_yield": [info.get('fiveYearAvgDividendYield', '')],
            "beta": [info.get('beta', '')],
            "trailing_pe": [info.get('trailingPE', '')],
            "forward_pe": [info.get('forwardPE', '')],
            "market_cap": [info.get('marketCap', '')],
            "price_to_sales_trailing_12_months": [info.get('priceToSalesTrailing12Months', '')],
            "trailing_annual_dividend_rate": [info.get('trailingAnnualDividendRate', '')],
            "trailing_annual_dividend_yield": [info.get('trailingAnnualDividendYield', '')],
            "enterprise_value": [info.get('enterpriseValue', '')],
            "profit_margins": [info.get('profitMargins', '')],
            "float_shares": [info.get('floatShares', '')],
            "shares_outstanding": [info.get('sharesOutstanding', '')],
            "shares_short": [info.get('sharesShort', '')],
            "shares_short_prior_month": [info.get('sharesShortPriorMonth', '')],
            "date_short_interest": [info.get('dateShortInterest', '')],
            "shares_percent_shares_out": [info.get('sharesPercentSharesOut', '')],
            "held_percent_insiders": [info.get('heldPercentInsiders', '')],
            "held_percent_institutions": [info.get('heldPercentInstitutions', '')],
            "short_ratio": [info.get('shortRatio', '')],
            "short_percent_of_float": [info.get('shortPercentOfFloat', '')],
            "implied_shares_outstanding": [info.get('impliedSharesOutstanding', '')],
            "book_value": [info.get('bookValue', '')],
            "price_to_book": [info.get('priceToBook', '')],
            "last_fiscal_year_end": [info.get('lastFiscalYearEnd', '')],
            "next_fiscal_year_end": [info.get('nextFiscalYearEnd', '')],
            "earnings_quarterly_growth": [info.get('earningsQuarterlyGrowth', '')],
            "trailing_eps": [info.get('trailingEps', '')],
            "forward_eps": [info.get('forwardEps', '')],
            "last_split_factor": [info.get('lastSplitFactor', '')],
            "last_split_date": [info.get('lastSplitDate', '')],
            "enterprise_to_revenue": [info.get('enterpriseToRevenue', '')],
            "enterprise_to_ebitda": [info.get('enterpriseToEbitda', '')],
            "last_dividend_value": [info.get('lastDividendValue', '')],
            "last_dividend_date": [info.get('lastDividendDate', '')],
            "exchange": [info.get('exchange', '')],
            "quote_type": [info.get('quoteType', '')],
            "symbol": [info.get('symbol', '')],
            "current_price": [info.get('currentPrice', '')],
            "target_high_price": [info.get('targetHighPrice', '')],
            "target_low_price": [info.get('targetLowPrice', '')],
            "target_mean_price": [info.get('targetMeanPrice', '')],
            "target_median_price": [info.get('targetMedianPrice', '')],
            "recommendation_mean": [info.get('recommendationMean', '')],
            "recommendation_key": [info.get('recommendationKey', '')],
            "number_of_analyst_opinions": [info.get('numberOfAnalystOpinions', '')],
            "total_cash": [info.get('totalCash', '')],
            "total_cash_per_share": [info.get('totalCashPerShare', '')],
            "ebitda": [info.get('ebitda', '')],
            "total_debt": [info.get('totalDebt', '')],
            "quick_ratio": [info.get('quickRatio', '')],
            "current_ratio": [info.get('currentRatio', '')],
            "total_revenue": [info.get('totalRevenue', '')],
            "debt_to_equity": [info.get('debtToEquity', '')],
            "revenue_per_share": [info.get('revenuePerShare', '')],
            "return_on_assets": [info.get('returnOnAssets', '')],
            "return_on_equity": [info.get('returnOnEquity', '')],
            "gross_profits": [info.get('grossProfits', '')],
            "free_cashflow": [info.get('freeCashflow', '')],
            "operating_cashflow": [info.get('operatingCashflow', '')],
            "earnings_growth": [info.get('earningsGrowth', '')],
            "revenue_growth": [info.get('revenueGrowth', '')],
            "gross_margins": [info.get('grossMargins', '')],
            "ebitda_margins": [info.get('ebitdaMargins', '')],
            "operating_margins": [info.get('operatingMargins', '')],
            "financial_currency": [info.get('financialCurrency', '')],
            "trailing_peg_ratio": [info.get('trailingPegRatio', '')],
            "last_updated": [datetime.now()]
        }
        '''
        data2 = {
            "Property": [],
            "Value": []
        }

        # Fill the dictionary with stock information
        for key, value in info.items():
            data2["Property"].append(key)
            data2["Value"].append(value)

        method = config.get('storage_method', 'csv')

        if method is None:
            # Default method is 'csv'
            method = 'csv'

        if method == 'csv':
            # Save to CSV
            # df = pd.DataFrame(data)
            df = pd.DataFrame(data2)

            csv_path = os.path.join(config.get('csv_data_dir', 'csv_data'), f"{ticker}_info.csv")
            df.to_csv(csv_path, mode='w', header=not pd.io.common.file_exists(csv_path), index=False)
            print(f"Data for {ticker} has been saved to CSV.")
        elif method == 'postgres':
            # Save to PostgreSQL
            stock_info, created = StockInfo.objects.update_or_create(
                ticker=ticker,
                defaults={key: value[0] for key, value in info.items()}
            )
            if created:
                print(f"New data for {ticker} has been saved to PostgreSQL.")
            else:
                print(f"Data for {ticker} has been updated in PostgreSQL.")
        else:
            print("Invalid storage method. Please choose either 'csv' or 'postgres'.")

    except Exception as e:
        print(f"Error fetching or saving data for {ticker}: {e}")


def store_analyst_recommendations(ticker, recommend, config):
    """
    Store the analyst recommendations either to a CSV file or a PostgreSQL database.

    Arguments:
    ticker (str) -- The stock ticker symbol.
    recommend (list of dicts) -- List of analyst recommendations with periods and ratings.
    config (dict) -- Configuration dictionary that specifies the storage method and file path.
    """
    method = config.get('storage_method', 'csv')

    if method == 'csv':
        # Save to CSV
        df = pd.DataFrame(recommend)
        csv_path = os.path.join(config.get('csv_data_dir', 'csv_data'), f"{ticker}_recommend.csv")

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['lastUpdated'] = current_time

        # Append data to CSV, with header only if the file doesn't exist yet
        df.to_csv(csv_path, mode='w', header=True, index=False)
        print(f"Data for {ticker} has been saved to CSV.")

    elif method == 'postgres':
        # Save to PostgreSQL database
        for entry in recommend:
            try:
                # Create a new AnalystRecommendation object and save it to the database
                AnalystRecommendation.objects.create(
                    ticker=ticker,
                    period=entry['period'],
                    strongBuy=entry['strongBuy'],
                    buy=entry['buy'],
                    hold=entry['hold'],
                    sell=entry['sell'],
                    strongSell=entry['strongSell']
                )
                print(f"Recommendation data for {ticker} in period {entry['period']} saved to PostgreSQL.")
            except IntegrityError:
                # This block handles the case where the combination of ticker and period already exists
                print(f"Data for {ticker} in period {entry['period']} already exists in the database. Skipping.")


# Main execution for testing purposes when this script is run directly
if __name__ == "__main__":
    # Choose a stock ticker symbol for testing
    ticker = "AAPL"  # Example: Apple Inc.

    from django.conf import settings

    # from core.data.fetcher import fetch_stock_data
    # print(f"Fetching and save historical data for {ticker}...")
    # historical_data = fetch_stock_data(ticker, period="5d", interval="1d")
    # store_stock_data(ticker, historical_data, settings.CONFIG)
    # print(historical_data)

    from fetcher import fetch_company_info

    print(f"\nFetching company information for {ticker}...")
    info = fetch_company_info(ticker)
    company_info = fetch_company_info(ticker, info, settings.CONFIG)
