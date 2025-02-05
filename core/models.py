"""
Define Django models for storing stock data when using PostgreSQL.
"""
from django.db import models

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
