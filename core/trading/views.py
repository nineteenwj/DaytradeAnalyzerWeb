"""
Trading simulation view.

This view processes simulation inputs for 5 groups.
For each simulation row, it:
  - Retrieves the selected date, buy price, stop loss, and take profit from POST data.
  - Calls get_local_data() (from core/utils.py) to obtain the 1-minute data for that ticker and date.
  - Passes the retrieved data to simulate_trade() to calculate the profit/loss percentage.
  - Returns a JSON response with the numeric result and its type.
"""

import os
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.trading.simulator import simulate_trade
from core.utils import get_local_data  # Ensure this function is defined in core/utils.py


@require_POST
def trading_index(request):
    print('---------In trading_index:', request.POST)
    sim_results = []
    # Retrieve ticker from hidden field
    ticker = request.POST.get("ticker_hidden")
    if not ticker:
        return JsonResponse({"error": "Ticker not provided."}, status=400)

    # Process each of the 5 simulation groups
    for i in range(1, 6):
        sim_date = request.POST.get(f"sim_date_{i}")  # Expected format: "YYYY-MM-DD"

        try:
            buy_price = float(request.POST.get(f"buy_price_{i}"))
            if buy_price == 0:
                result_value = 0
            else:
                stop_loss = float(request.POST.get(f"stop_loss_{i}"))
                take_profit = float(request.POST.get(f"take_profit_{i}"))

                # Retrieve 1-minute data for the given ticker and date
                minute_data = get_local_data(ticker, date=sim_date)

                # Pass the retrieved data to simulate_trade
                result_value = simulate_trade(buy_price, stop_loss, take_profit, minute_data)

            # Determine result type based on the numeric value
            if result_value > 0:
                result_type = "positive"
            elif result_value < 0:
                result_type = "negative"
            else:
                result_type = "neutral"
        except Exception:
            result_value = None
            result_type = "neutral"

        sim_results.append({
            "date": sim_date,
            "result": result_value,
            "result_type": result_type
        })
    print('------sim_result:', sim_results)
    return JsonResponse({"sim_results": sim_results})
