from django.urls import path

from .views import *

urlpatterns = [
    path('fetch/', fetch_data,name='fetch'),
    path('backtest', run_backtest, name='run_backtest'),
    path('predict/', predict_stock_prices, name='predict_stock_prices'),
    path('report/',report , name='report'),
    path('api/',api , name='api')
]