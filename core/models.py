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

    def __str__(self):
        return f"{self.ticker} - {self.date.strftime('%Y-%m-%d %H:%M')}"


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

