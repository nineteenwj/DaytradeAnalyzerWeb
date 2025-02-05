"""
Define tests for the core app.
For brevity, only a simple test is provided.
"""
from django.test import TestCase
from .models import StockData

class StockDataModelTest(TestCase):
    def test_str(self):
        # Create a dummy StockData object
        data = StockData.objects.create(
            ticker="AAPL",
            date="2023-01-01T10:00:00Z",
            open=150.0,
            high=155.0,
            low=149.0,
            close=154.0,
            volume=1000000
        )
        self.assertIn("AAPL", str(data))
