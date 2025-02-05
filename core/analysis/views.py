"""
Analysis view for DayTrade Analyzer Web.

This view uses two separate forms:
  - TickerForm: used to input a stock ticker and fetch data from the network.
  - DateRangeForm: used to select a date range from available local data (using drop-down menus).

Actions:
1. When the "GET STOCK DATA" button is pressed:
   - Process TickerForm to get the ticker.
   - Fetch stock data using yfinance (1-minute interval for the last 7 days).
   - Store the fetched data locally (CSV or PostgreSQL based on configuration).
   - Read the local data to extract the available dates.
   - Set the available dates as choices for the start_date and end_date fields of DateRangeForm.
2. When the "SHOW CANDLESTICK" button is pressed:
   - Process DateRangeForm to get the selected start_date and end_date.
   - Retrieve the ticker from a hidden field.
   - Load the local data, filter it by the selected date range, and generate a candlestick chart.
   - Update the available date options and pass the chart image to the template.
"""

import os
import pandas as pd
from django.shortcuts import render
from django.contrib import messages
from core.forms import TickerForm, DateRangeForm
from core.data.fetcher import fetch_stock_data
from core.data.storage import store_stock_data
from core.analysis.chart import generate_candlestick_chart
from django.conf import settings
from core.utils import get_local_data


def analysis_index(request):
    context = {}
    # Initialize both forms: one for ticker input and one for selecting date range.
    ticker_form = TickerForm()
    date_range_form = DateRangeForm()  # This form uses ChoiceField for start_date and end_date.

    if request.method == "POST":
        if "get_stock_data" in request.POST:
            # Process the GET STOCK DATA action.
            ticker_form = TickerForm(request.POST)
            if ticker_form.is_valid():
                ticker = ticker_form.cleaned_data["ticker"]
                try:
                    # Fetch stock data (1-minute interval, last 7 days)
                    data = fetch_stock_data(ticker, period="7d", interval="1m")
                    # Store the fetched data locally (CSV or PostgreSQL as per configuration)
                    store_stock_data(data, ticker, settings.CONFIG)
                    messages.success(request, "Stock data fetched and stored successfully.")

                    # Read local data to extract available dates.
                    if settings.CONFIG.get("storage_method") == "csv":
                        csv_path = os.path.join(settings.BASE_DIR, settings.CONFIG.get("csv_data_dir", "csv_data"),
                                                f"{ticker}.csv")
                        local_data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
                    else:
                        from core.models import StockData
                        qs = StockData.objects.filter(ticker=ticker).order_by("date")
                        local_data = pd.DataFrame(list(qs.values("date", "open", "high", "low", "close", "volume")))
                        local_data["date"] = pd.to_datetime(local_data["date"])
                        local_data.set_index("date", inplace=True)

                    # Extract unique dates from the local data
                    date_list = sorted({d.strftime("%Y-%m-%d") for d in local_data.index})
                    context["date_options"] = date_list
                    context["ticker"] = ticker

                    # Dynamically set the choices for start_date and end_date fields in DateRangeForm.
                    date_choices = [(d, d) for d in date_list]
                    date_range_form.fields["start_date"].choices = date_choices
                    date_range_form.fields["end_date"].choices = date_choices
                except Exception as e:
                    messages.error(request, f"Error fetching data: {e}")
            else:
                messages.error(request, "Invalid input for ticker.")
            context["ticker_form"] = ticker_form
            context["date_range_form"] = date_range_form

        elif "show_candlestick" in request.POST:
            # Get the ticker from a hidden field
            ticker = request.POST.get("ticker_hidden")
            chosen_interval = request.POST.get("interval", "1m")  # Default to "1m" if not provided

            # First, extract the date_list from your local data (after loading local_data)
            local_data = get_local_data(ticker)
            date_list = sorted({d.strftime("%Y-%m-%d") for d in local_data.index})
            # Create choices as a list of tuples
            date_choices = [(d, d) for d in date_list]  # date_list extracted from local data
            # Instantiate DateRangeForm with the dynamic choices
            date_range_form = DateRangeForm(request.POST, date_choices=date_choices)

            if date_range_form.is_valid():
                start_date = date_range_form.cleaned_data["start_date"]
                end_date = date_range_form.cleaned_data["end_date"]
                if not ticker:
                    messages.error(request, "Ticker not provided.")
                else:
                    try:
                        if settings.CONFIG.get("storage_method") == "csv":
                            csv_path = os.path.join(settings.BASE_DIR, settings.CONFIG.get("csv_data_dir", "csv_data"),
                                                    f"{ticker}.csv")
                            local_data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
                        else:
                            from core.models import StockData
                            qs = StockData.objects.filter(ticker=ticker).order_by("date")
                            local_data = pd.DataFrame(list(qs.values("date", "open", "high", "low", "close", "volume")))
                            local_data["date"] = pd.to_datetime(local_data["date"])
                            local_data.set_index("date", inplace=True)

                        # Ensure the index is datetime
                        local_data.index = pd.to_datetime(local_data.index)
                        # Filter local data by the selected date range.
                        mask = (local_data.index.date >= pd.to_datetime(start_date).date()) & (
                                    local_data.index.date <= pd.to_datetime(end_date).date())
                        filtered = local_data.loc[mask]
                        if filtered.empty:
                            messages.error(request, "No data available for the selected date range.")
                        else:
                            # If the chosen interval is not 1m, resample the filtered data accordingly.
                            if chosen_interval != "1m":
                                resample_map = {
                                    "5m": "5T",
                                    "15m": "15T",
                                    "30m": "30T",
                                    "1h": "1H",
                                    "1d": "1D"
                                }
                                if chosen_interval in resample_map:
                                    filtered = filtered.resample(resample_map[chosen_interval]).agg({
                                        "Open": "first",
                                        "High": "max",
                                        "Low": "min",
                                        "Close": "last",
                                        "Volume": "sum"
                                    }).dropna()
                            # Generate the candlestick chart image (base64 encoded).
                            img = generate_candlestick_chart(filtered, ticker)
                            context["chart"] = img
                            # Build a price list: each entry contains date, open, high, low, close.
                            price_list = []
                            # only when interval is 1d shows detail price list
                            if chosen_interval == "1d":
                                for dt, row in filtered.iterrows():
                                    price_list.append({
                                        "date": dt.strftime("%Y-%m-%d"),
                                        "open": round(row["Open"],2),
                                        "high": round(row["High"],2),
                                        "low": round(row["Low"],2),
                                        "close": round(row["Close"],2),
                                    })
                            context["price_list"] = price_list
                        # Update available dates.
                        date_list = sorted({d.strftime("%Y-%m-%d") for d in local_data.index})
                        context["date_options"] = date_list
                        context["ticker"] = ticker
                        # Update the DateRangeForm choices.
                        date_choices = [(d, d) for d in date_list]
                        date_range_form.fields["start_date"].choices = date_choices
                        date_range_form.fields["end_date"].choices = date_choices
                    except Exception as e:
                        messages.error(request, f"Error displaying chart: {e}")
            else:
                messages.error(request, "Invalid date range input.")
            context["ticker_form"] = ticker_form
            context["date_range_form"] = date_range_form

    else:
        # For GET requests, initialize empty forms.
        context["ticker_form"] = ticker_form
        context["date_range_form"] = date_range_form

    return render(request, "core/index.html", context)
