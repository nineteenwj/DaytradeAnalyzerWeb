"""
Views for the stock list page.

This module displays a list of locally stored stocks with their data range
and provides a form to add a new stock. It uses the data-related methods from the
'core/data' package.
"""

import os
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from core.data.querier import get_all_stock_list
from core.trading.strategies import TRADING_STRATEGIES
from core.data.fetcher import fetch_stock_data
from core.data.storage import store_stock_data


def dashboard_view(request):
    """
    Display a list of stocks from local storage.

    Also, provides a form in the top-right to add a new stock. If the stock is already in the list,
    an error message is displayed.
    """
    stocks = get_all_stock_list()
    strategies = TRADING_STRATEGIES

    context = {
        "stocks": stocks,
        'strategies': strategies
    }

    # Process new stock addition if submitted
    if request.method == "POST" and "new_stock" in request.POST:
        new_stock = request.POST.get("new_stock", "").strip().upper()
        result = add_stock(new_stock)
        if result['ret']:
            messages.success(request, result['msg'])
        else:
            messages.error(request, result['msg'])
        return redirect("index")
    return render(request, "core/index.html", context)


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
            # Fetch and store stock data (1-minute data, 7 days)
            data = fetch_stock_data(new_stock, period="7d", interval="1m")
            store_stock_data(new_stock, data, settings.CONFIG)
            msg = f"{new_stock} has been added successfully."
            ret = True
        except Exception as e:
            msg = f"Error adding {new_stock}: {e}"
            print(msg)
    return {'ret': ret, 'msg': msg}


def update_stock(request, ticker):
    """
    Update stock data for the given ticker.
    This view fetches new stock data from the network and updates local storage.
    After updating, it redirects back to the stock list page.
    """
    if request.method == "POST":
        try:
            data = fetch_stock_data(ticker, period="7d", interval="1m")
            store_stock_data(ticker, data, settings.CONFIG)
            messages.success(request, f"{ticker} data updated successfully.")
        except Exception as e:
            messages.error(request, f"Error updating {ticker} data: {e}")
    else:
        messages.error(request, "Invalid request method.")
    return redirect("index")


def stock_info_view(request, ticker_code):
    # 获取指定股票的 StockInfo
    from core.data.fetcher import fetch_company_info, fetch_analyst_recommendations
    from core.data.storage import store_stock_info, store_analyst_recommendations

    stock_info = fetch_company_info(ticker_code)
    store_stock_info(ticker_code, stock_info, settings.CONFIG)

    recommendations = fetch_analyst_recommendations(ticker_code)
    store_analyst_recommendations(ticker_code, recommendations, settings.CONFIG)

    periods_meaning = {
        '0m': '本月',
        '-1m': '1个月前',
        '-2m': '2个月前',
        '-3m': '3个月前'
    }

    # Preprocess the recommendations to include period meanings
    for recommendation in recommendations:
        recommendation['period_meaning'] = periods_meaning.get(recommendation['period'])

    return render(request, 'core/stock_info.html', {'stock_info': stock_info, 'stock_recommendations': recommendations})
