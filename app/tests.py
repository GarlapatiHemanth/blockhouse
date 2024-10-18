from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import stockPricesData
from .views import backtest_strategy

class BacktestTests(TestCase):
    def setUp(self):
        # Create some sample stock price data for testing
        stockPricesData.objects.create(symbol='IBM', date='2024-01-01',open_price=145, close_price=150.0, high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-02',open_price=145, close_price=151.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-03',open_price=145, close_price=150.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-04',open_price=145, close_price=149.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-05',open_price=145, close_price=154.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-06',open_price=145, close_price=155.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-07',open_price=145, close_price=156.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-08',open_price=145, close_price=157.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-09',open_price=145, close_price=158.0,high_price= 150,low_price=145, volume=1000)
        # Add more data as needed...

    def test_backtest_strategy(self):
        result = backtest_strategy('IBM', 1500,2,3)
        print(result)
        self.assertIn('total_return', result)
        self.assertIn('max_drawdown', result)
        self.assertIn('number_of_trades', result)

