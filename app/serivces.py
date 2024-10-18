
import pandas as pd
from datetime import datetime,timedelta
from .models import stockPricesData
import requests
from django.conf import settings
from .exceptions import *
from django.http import JsonResponse
from .ml import trainmodel
import pickle


def fetch_stock_data(symbol):

    data= stockPricesData.objects.filter(symbol=symbol, type='A')
   
    if data:
        return data
    else :
        try:
            data=alpha_api_call(symbol)
            print(data)
            
        except Exception as e:
         
            return StockDataError(e)
    

    if data :
        

        time_series = data.get("Time Series (Daily)", {})

        current_date = datetime.strptime(data['Meta Data']['3. Last Refreshed'], '%Y-%m-%d')
        two_years_ago = current_date - timedelta(days=2*365)    
    
    

        for date_str, daily_data in time_series.items():
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            if date_obj >= two_years_ago:
            
            
                stockPricesData.objects.update_or_create(
                symbol=symbol,  
                date=date_obj,
                defaults={
                'open_price': daily_data['1. open'],
                'close_price': daily_data['4. close'],
                'high_price': daily_data['2. high'],
                'low_price': daily_data['3. low'],
                'volume': daily_data['5. volume']
                })
    return stockPricesData.objects.filter(symbol=symbol,type='A')
        

def alpha_api_call(symbol):
    
    try: 
        print(get_alpha_api_parms(symbol))
        response = requests.get(settings.ALPHA_BASE_URL, params=get_alpha_api_parms(symbol))
        return response.json()
    except Exception as e:
        print('2')
        print('error ',str(e))
        return StockDataError(e)


def get_alpha_api_parms(symbol):
    params = {
            "function":  settings.ALPHA_FUNCTION,
            "symbol": symbol,
            "apikey": settings.ALPHA_VANTAGE_API_KEY,
            "outputsize": settings.ALPHA_OUTPUT_SIZE
        }
    
    return params


def backtest_strategy(symbol, initial_investment, ma_short=50, ma_long=200):
    
    stock_data = fetch_stock_data(symbol).order_by('date')
  
    df = pd.DataFrame(list(stock_data.values()))
    
    if df.empty:
        raise StockDataError(f"No data available for symbol: {symbol}")
   
    
    df['ma_short'] = df['close_price'].rolling(window=ma_short).mean()
    df['ma_long'] = df['close_price'].rolling(window=ma_long).mean()

    
    df = df.dropna(subset=['ma_short', 'ma_long'])

    
    if df.empty:
        raise StockDataError(f"Not enough data after calculating moving averages for symbol: {symbol}")

    
    investment = initial_investment
    shares_owned = 0
    trades = 0
    max_drawdown = 0
    peak = investment
    
    # Backtesting logic
    for index in range(len(df)):
        # Buy signal
        if df['close_price'].iloc[index] < df['ma_short'].iloc[index] and shares_owned == 0:
            shares_owned = investment // df['close_price'].iloc[index]  
            investment -= shares_owned * df['close_price'].iloc[index]
            trades += 1
           

        # Sell signal
        elif df['close_price'].iloc[index] > df['ma_long'].iloc[index] and shares_owned > 0:
            investment += shares_owned * df['close_price'].iloc[index]
            shares_owned = 0  
            trades += 1
           

        if investment > peak:
            peak = investment
        
        drawdown = (peak - investment) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    total_return = (investment + (shares_owned * df['close_price'].iloc[-1])) - initial_investment

    return {
        "total_return": total_return,
        "max_drawdown": max_drawdown,
        "number_of_trades": trades,
    }




def predict_next_30_days_and_store(symbol):
    
    data = fetch_stock_data(symbol)
    trainmodel(data)

    with open('linear_regression_model.pkl', 'rb') as file:
        model = pickle.load(file)

   
    
    data = list(data.values('date', 'close_price'))
    df = pd.DataFrame(data)

    
    last_date = pd.to_datetime(df['date'].max())

  
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30, freq='D')

    
    future_dates_ordinal = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    
    future_predictions = model.predict(future_dates_ordinal)

    
    predictions_df = pd.DataFrame({
    
        'date': future_dates,
        'predicted_close_price': future_predictions
    })

    predictions_df['date'] = predictions_df['date'].dt.strftime('%Y-%m-%d')


    
    for _, row in predictions_df.iterrows():
        stockPricesData.objects.update_or_create(
            symbol=symbol,
            date=row['date'],

            defaults={
                    'close_price': row['predicted_close_price'],
                    'type': 'P'  
                }
        )


    return predictions_df

