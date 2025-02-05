"""
Register models in the Django admin site.
"""
from django.contrib import admin
from .models import StockData

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'date', 'open', 'high', 'low', 'close', 'volume')
