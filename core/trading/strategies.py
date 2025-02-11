
class Strategy:
    def __init__(self, id, name, description, url, status):
        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.status = status

TRADING_STRATEGIES = [
    Strategy(
        1,
        "Opening buy strategy",
        "Short-Term Quick Action Strategy After Market Open",
        "opening_buy_strategy",
        "active"
    ),
    Strategy(
        2,
        "Swing buy strategy",
        "Intraday Swing Trading Strategy",
        "swing_buy_strategy",
        "testing"
    ),
    Strategy(
        3,
        "MACD Strategy",
        "",
        "opening_buy_strategy",
        "inactive"
    )
]