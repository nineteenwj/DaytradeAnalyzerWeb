"""
Module to simulate trades based on 1-minute data.

This function now expects the minute-level data to be passed as an argument.
It iterates over the data (for a given date) and compares the buy_price
with each minute's Open, Low, High, and Close in order.
If a condition is met, it returns the profit/loss percentage:
  - A positive number indicates take profit.
  - A negative number indicates stop loss.
If no condition is met across all minutes, it returns 0.
"""

def simulate_trade(buy_price, stop_loss, take_profit, minute_data):
    """
    Simulate a trade for the given minute-level data.

    Parameters:
      buy_price (float): The buy price.
      stop_loss (float): Stop loss threshold percentage (e.g., 5 means 5%).
      take_profit (float): Take profit threshold percentage (e.g., 5 means 5%).
      minute_data (DataFrame): A pandas DataFrame containing 1-minute data
                               for a specific date. Must include columns 'Open', 'Low', 'High', 'Close'.

    Returns:
      float: The profit/loss percentage that triggered the sell.
             A positive value for profit, negative for loss, or 0 if no condition met.
    """
    # Iterate over each minute's data in chronological order
    for idx, row in minute_data.iterrows():
        # Check the prices in the order: Open, Low, High, Close
        prices = [row['Open'], row['Low'], row['High'], row['Close']]
        for price in prices:
            if price < buy_price:
                loss_pct = (buy_price - price) / buy_price * 100.0
                if loss_pct > stop_loss:
                    return -round(loss_pct, 2)
            elif price > buy_price:
                profit_pct = (price - buy_price) / buy_price * 100.0
                if profit_pct > take_profit:
                    return round(profit_pct, 2)
        # Continue to next minute if no condition met
    return 0.0
