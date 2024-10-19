from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import stockPricesData
from unittest.mock import patch, MagicMock
from .models import stockPricesData
from .views import fetch_stock_data, backtest_strategy, predict_next_30_days_and_store
from .exceptions import StockDataError
import pandas as pd
from datetime import datetime

class BacktestTests(TestCase):
    def setUp(self):
        
        stockPricesData.objects.create(symbol='IBM', date='2024-01-01',open_price=145, close_price=150.0, high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-02',open_price=145, close_price=151.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-03',open_price=145, close_price=150.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-04',open_price=145, close_price=149.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-05',open_price=145, close_price=154.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-06',open_price=145, close_price=155.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-07',open_price=145, close_price=156.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-08',open_price=145, close_price=157.0,high_price= 150,low_price=145, volume=1000)
        stockPricesData.objects.create(symbol='IBM', date='2024-01-09',open_price=145, close_price=158.0,high_price= 150,low_price=145, volume=1000)
       

    def test_backtest_strategy(self):
        result = backtest_strategy('IBM', 1500,2,3)
        
        self.assertEqual(result['total_return'],40.00)



class StockDataTestCase(TestCase):
    
    def setUp(self):
        
        stockPricesData.objects.create(
            symbol='AAPL', 
            date=datetime.now(), 
            open_price=150.0, 
            close_price=155.0, 
            high_price=157.0, 
            low_price=149.0, 
            volume=10000,
            type='A'
        )

    @patch('app.views.alpha_api_call')
    def test_fetch_stock_data_with_existing_data(self, mock_alpha_api_call):
      
        result = fetch_stock_data('AAPL')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].symbol, 'AAPL')

    @patch('app.views.alpha_api_call')
    def test_fetch_stock_data_error(self, mock_alpha_api_call):
       
        mock_alpha_api_call.side_effect = Exception("API Error")
        result = fetch_stock_data('INVALID')
        self.assertIsInstance(result, StockDataError)

 
    
    @patch('app.views.trainmodel')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('pickle.load')
    def test_predict_next_30_days_and_store(self, mock_pickle_load, mock_open, mock_trainmodel):
       
        mock_model = MagicMock()
        mock_pickle_load.return_value = mock_model
        mock_model.predict.return_value = [150.0] * 30 

        result = predict_next_30_days_and_store('AAPL')
        self.assertEqual(len(result), 30)
        self.assertIn('predicted_close_price', result.columns)


