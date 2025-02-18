"""
Define Django models for storing stock data when using PostgreSQL.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    market = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"{self.ticker} - {self.date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        # Ensure that records are ordered by date and ticker code
        ordering = ['ticker', 'date']
        # Add an index for faster querying by ticker_code and date
        indexes = [
            models.Index(fields=['ticker', 'date']),
        ]

class StockInfo(models.Model):
    ticker = models.CharField(max_length=10, unique=True)  # Stock ticker symbol
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    long_business_summary = models.TextField(blank=True, null=True)
    full_time_employees = models.IntegerField(null=True, blank=True)
    audit_risk = models.IntegerField(null=True, blank=True)
    board_risk = models.IntegerField(null=True, blank=True)
    compensation_risk = models.IntegerField(null=True, blank=True)
    share_holder_rights_risk = models.IntegerField(null=True, blank=True)
    overall_risk = models.IntegerField(null=True, blank=True)
    dividend_rate = models.FloatField(null=True, blank=True)
    dividend_yield = models.FloatField(null=True, blank=True)
    ex_dividend_date = models.DateTimeField(null=True, blank=True)
    payout_ratio = models.FloatField(null=True, blank=True)
    five_year_avg_dividend_yield = models.FloatField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    trailing_pe = models.FloatField(null=True, blank=True)
    forward_pe = models.FloatField(null=True, blank=True)
    market_cap = models.BigIntegerField(null=True, blank=True)
    price_to_sales_trailing_12_months = models.FloatField(null=True, blank=True)
    trailing_annual_dividend_rate = models.FloatField(null=True, blank=True)
    trailing_annual_dividend_yield = models.FloatField(null=True, blank=True)
    enterprise_value = models.BigIntegerField(null=True, blank=True)
    profit_margins = models.FloatField(null=True, blank=True)
    float_shares = models.BigIntegerField(null=True, blank=True)
    shares_outstanding = models.BigIntegerField(null=True, blank=True)
    shares_short = models.BigIntegerField(null=True, blank=True)
    shares_short_prior_month = models.BigIntegerField(null=True, blank=True)
    date_short_interest = models.DateTimeField(null=True, blank=True)
    shares_percent_shares_out = models.FloatField(null=True, blank=True)
    held_percent_insiders = models.FloatField(null=True, blank=True)
    held_percent_institutions = models.FloatField(null=True, blank=True)
    short_ratio = models.FloatField(null=True, blank=True)
    short_percent_of_float = models.FloatField(null=True, blank=True)
    implied_shares_outstanding = models.BigIntegerField(null=True, blank=True)
    book_value = models.FloatField(null=True, blank=True)
    price_to_book = models.FloatField(null=True, blank=True)
    last_fiscal_year_end = models.DateTimeField(null=True, blank=True)
    next_fiscal_year_end = models.DateTimeField(null=True, blank=True)
    earnings_quarterly_growth = models.FloatField(null=True, blank=True)
    trailing_eps = models.FloatField(null=True, blank=True)
    forward_eps = models.FloatField(null=True, blank=True)
    last_split_factor = models.CharField(max_length=10, blank=True, null=True)
    last_split_date = models.DateTimeField(null=True, blank=True)
    enterprise_to_revenue = models.FloatField(null=True, blank=True)
    enterprise_to_ebitda = models.FloatField(null=True, blank=True)
    last_dividend_value = models.FloatField(null=True, blank=True)
    last_dividend_date = models.DateTimeField(null=True, blank=True)
    exchange = models.CharField(max_length=20, blank=True, null=True)
    quote_type = models.CharField(max_length=20, blank=True, null=True)
    symbol = models.CharField(max_length=10, unique=True)
    current_price = models.FloatField(null=True, blank=True)
    target_high_price = models.FloatField(null=True, blank=True)
    target_low_price = models.FloatField(null=True, blank=True)
    target_mean_price = models.FloatField(null=True, blank=True)
    target_median_price = models.FloatField(null=True, blank=True)
    recommendation_mean = models.FloatField(null=True, blank=True)
    recommendation_key = models.CharField(max_length=20, blank=True, null=True)
    number_of_analyst_opinions = models.IntegerField(null=True, blank=True)
    total_cash = models.BigIntegerField(null=True, blank=True)
    total_cash_per_share = models.FloatField(null=True, blank=True)
    ebitda = models.BigIntegerField(null=True, blank=True)
    total_debt = models.BigIntegerField(null=True, blank=True)
    quick_ratio = models.FloatField(null=True, blank=True)
    current_ratio = models.FloatField(null=True, blank=True)
    total_revenue = models.BigIntegerField(null=True, blank=True)
    debt_to_equity = models.FloatField(null=True, blank=True)
    revenue_per_share = models.FloatField(null=True, blank=True)
    return_on_assets = models.FloatField(null=True, blank=True)
    return_on_equity = models.FloatField(null=True, blank=True)
    gross_profits = models.BigIntegerField(null=True, blank=True)
    free_cashflow = models.BigIntegerField(null=True, blank=True)
    operating_cashflow = models.BigIntegerField(null=True, blank=True)
    earnings_growth = models.FloatField(null=True, blank=True)
    revenue_growth = models.FloatField(null=True, blank=True)
    gross_margins = models.FloatField(null=True, blank=True)
    ebitda_margins = models.FloatField(null=True, blank=True)
    operating_margins = models.FloatField(null=True, blank=True)
    financial_currency = models.CharField(max_length=3, blank=True, null=True)
    trailing_peg_ratio = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker

    class Meta:
        ordering = ['ticker', '-last_updated']
        indexes = [
            models.Index(fields=['ticker']),
        ]

class AnalystRecommendation(models.Model):
    ticker = models.CharField(max_length=10)  # 存储股票代码
    period = models.CharField(max_length=10)  # 存储时间段，例如 '0m', '-1m', '-2m', '-3m'
    strongBuy = models.IntegerField(default=0)  # 强买推荐数
    buy = models.IntegerField(default=0)  # 买推荐数
    hold = models.IntegerField(default=0)  # 持有推荐数
    sell = models.IntegerField(default=0)  # 卖推荐数
    strongSell = models.IntegerField(default=0)  # 强卖推荐数
    last_updated = models.DateTimeField(auto_now=True)  # 记录最后更新时间

    class Meta:
        unique_together = ('ticker', 'period')  # 确保每个股票和时间段的记录唯一

    def __str__(self):
        return f"{self.ticker} - {self.period}"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    reset_password_expire = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username

class TradingOpening(models.Model):
    date = models.DateField()
    pc_code = models.CharField(max_length=10)
    strategy = models.CharField(max_length=50)
    strategy_result = models.FloatField()  # 盈亏百分比
    pc_code_refer_price = models.FloatField()
    buy_code = models.CharField(max_length=10)
    buy_price_up_ratio = models.FloatField()
    buy_price = models.FloatField()
    quantity = models.IntegerField()
    take_profit = models.FloatField()
    stop_loss = models.FloatField()
    sell_price = models.FloatField()
    profit_loss_ratio = models.FloatField()
    profit_loss = models.FloatField()
    sell_time = models.DateField()

    def __str__(self):
        return f"{self.date} - {self.pc_code} - {self.buy_code}"

