"""
Module to generate candlestick charts.
Generates a chart image (as base64-encoded PNG) from stock data.
"""
import matplotlib

matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import io
import base64


def generate_candlestick_chart(data, ticker):
    """
    Generate a candlestick chart from the provided data.

    Parameters:
      data (DataFrame): The stock data.
      ticker (str): The stock ticker symbol.

    Returns:
      str: Base64-encoded PNG image of the chart.
    """
    data = data.copy()
    data.index.name = 'Date'
    data.reset_index(inplace=True)
    data['Date'] = mdates.date2num(data['Date'])
    ohlc = data[['Date', 'Open', 'High', 'Low', 'Close']].values

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4), sharex=True)
    candlestick_ohlc(ax1, ohlc, width=0.005, colorup='g', colordown='r')
    ax2.bar(data['Date'], data['Volume'], color='blue', width=0.005)
    ax1.xaxis_date()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    fig.suptitle(f"Stock Data for {ticker}", fontsize=10)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64
