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
from core.data.querier import get_all_stock_list, add_stock
from core.trading.strategies import TRADING_STRATEGIES


def dashboard(request):
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



def update_stock(request, ticker):
    """
    Update stock data for the given ticker.
    This view fetches new stock data from the network and updates local storage.
    After updating, it redirects back to the stock list page.
    """
    if request.method == "POST":
        try:
            from core.data.fetcher import fetch_stock_data
            from core.data.storage import store_stock_data
            data = fetch_stock_data(ticker, period="7d", interval="1m")
            store_stock_data(data, ticker, settings.CONFIG)
            messages.success(request, f"{ticker} data updated successfully.")
        except Exception as e:
            messages.error(request, f"Error updating {ticker} data: {e}")
    else:
        messages.error(request, "Invalid request method.")
    return redirect("index")
