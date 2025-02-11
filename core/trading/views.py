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
from django.conf import settings
from django.shortcuts import render
from core.data.querier import get_local_data, query_local_stock_data, get_stock_info_by_date, get_all_stock_list
import json
from core.forms import TradingOpeningForm
from .strategies import TRADING_STRATEGIES
from datetime import timedelta

def get_trading_strategies():
    return TRADING_STRATEGIES



def swing_buy_strategy(request):
    if request.method == 'GET':
        return render(request, "core/trading/swing_buy_strategy.html", {"sim_results": ''})
    else:
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
        #return JsonResponse({"sim_results": sim_results})
        return render(request, "core/trading/swing_buy_strategy.html", {"sim_results": sim_results})


def opening_buy_strategy(request):
    stocks = get_all_stock_list()

    form = TradingOpeningForm()

    context = {
        "stocks": stocks,
        "form":form,
    }
    return render(request, "core/trading/opening_buy_strategy.html", context)


def query_stock_data(request):
    if request.method == 'POST':
        print('In query_stock_data:', request.POST)
        # 获取用户输入的参数
        ticker = request.POST.get('query_stock_code')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        price_data = []
        current_date = start_date

        while current_date <= end_date:
            info = get_stock_info_by_date(ticker, current_date)
            price_data.append({
                'date': info['date'],
                'pre_market_open': info['pre_market_open'],
                'pre_market_close': info['pre_market_close'],
                'pre_market_change': f'{info["pre_market_change"]:.2f}%',
                'intraday_open': info['intraday_open'],
                'intraday_close': info['intraday_close'],
                'intraday_change': f'{info["intraday_change"]:.2f}%'
            })

            current_date += timedelta(days=1)

        print('------------price_data:', price_data)
        # 返回 JSON 响应
        return JsonResponse(json.dumps(price_data), safe=False)

    return render(request, 'trading/opening_buy_strategy.html')

def opening_auto_simulation(request):
    if request.method == 'POST':
        print('In opening_auto_simulation:', request.POST)
        results = []

        form = TradingOpeningForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            pc_code = form.cleaned_data['pc_code']
            strategy = form.cleaned_data['strategy']
            buy_code1 = form.cleaned_data['buy_code1']
            buy_code2 = form.cleaned_data['buy_code2']
            buy_price_up_ratio = form.cleaned_data['buy_price_up_ratio']
            quantity = form.cleaned_data['quantity']
            take_profit = form.cleaned_data['take_profit']
            stop_loss = form.cleaned_data['stop_loss']
            buy_code = buy_code1

            current_date = start_date
            while current_date <= end_date:
                current_date_str = current_date.strftime('%Y-%m-%d')
                if strategy == 'Pre-market Close':
                    retVal = get_stock_info_by_date(pc_code, current_date_str)
                    if not retVal:# current_date取不到数据，说明此非交易日，继续下一轮循环
                        current_date += timedelta(days=1)
                        continue
                    else:
                        refer_ratio = round(retVal['pre_market_change'],2)
                    if refer_ratio >= 0:
                        buy_code = buy_code1
                    else:
                        buy_code = buy_code2
                    retVal = query_local_stock_data(buy_code, current_date_str, current_date_str, '1d')
                    # current_date取不到数据，说明此非交易日，继续下一轮循环
                    if not retVal:
                        current_date += timedelta(days=1)
                        continue
                    else:
                        refer_price = retVal[0]['markets']['pre-market']['Close']
                elif strategy == 'Pre-market Avg':
                    # 获取盘前平均价格
                    refer_price = 0
                elif strategy == 'Pre-market Weighted':
                    # 获取加权平均价格
                    refer_price = 0
                elif strategy == 'Intraday Open':
                    refer_price = get_stock_info_by_date(pc_code, current_date_str)['intraday_Open']
                else:
                    refer_price = 0  # 默认参考价格

                # Retrieve 1-minute data for the given ticker and date
                minute_data = get_local_data(buy_code, date=current_date_str, market='intraday')
                # 购买价为盘前收盘价 上浮一定比率
                buy_price = round(refer_price * (1+buy_price_up_ratio),2)

                result_value = simulate_trade(buy_price, stop_loss, take_profit, minute_data)
                profit_loss_ratio = round(result_value['profit_loss'],2)
                profit_loss = round(profit_loss_ratio * buy_price*quantity / 100, 2)

                retVal = {'date': current_date,
                          'pc_code': pc_code,
                          'strategy': strategy,
                          'strategy_result': refer_ratio,
                          'pc_code_refer_price': refer_price,
                          'buy_code': buy_code,
                          'buy_price_up_ratio': buy_price_up_ratio,
                          'buy_price': buy_price,
                          'quantity': quantity,
                          'take_profit': take_profit,
                          'stop_loss': stop_loss,
                          'sell_price': result_value['sell_price'],
                          'profit_loss_ratio': profit_loss_ratio,
                          'profit_loss': profit_loss,
                          'sell_time': result_value['sell_time'],
                          }


                results.append(retVal)

                current_date += timedelta(days=1)
            print('--------------------', results)

            return JsonResponse({'results': results})

    else:
        form = TradingForm()

    return render(request, 'trading/opening_buy_strategy.html', {'form': form})


def calculate_profitloss(request):
    if request.method == 'POST':
        requestParam = request.POST.get('trade_data')
        print('In calculateProfitLoss requestParam:', requestParam)
        trade_list = json.loads(requestParam)
        print('In calculateProfitLoss:', trade_list)
        sim_results = []

        status = 'failure'

        for trade in trade_list:
            result_value = 0
            date = trade['date']
            pcondition_code = trade['precon_code']
            strategy = trade['strategy']
            buy_code = trade['buy_code']
            buy_price = float(trade['buy_price'])
            quantity = int(trade['quantity'])
            try:
                if buy_price == 0:
                    result_value = 0
                else:
                    take_profit = float(trade['take_profit'])
                    stop_loss = float(trade['stop_loss'])

                    # Retrieve 1-minute data for the given ticker and date
                    minute_data = get_local_data(buy_code, date=date, market='intraday')
                    # Pass the retrieved data to simulate_trade
                    result_value = simulate_trade(buy_price, stop_loss, take_profit, minute_data)
                    # Determine result type based on the numeric value
                    if result_value['profit_loss'] > 0:
                        result_type = "positive"
                    elif result_value['profit_loss'] < 0:
                        result_type = "negative"
                    else:
                        result_type = "neutral"
                status = 'success'
            except Exception:
                result_value = None
                result_type = "neutral"

            sim_results.append({
                "result": result_value,
                "result_type": result_type,
            })
        retVal = {"status": status, "simulate": sim_results}
        print('------sim_result:', retVal)

    return JsonResponse(json.dumps(retVal), safe=False)
