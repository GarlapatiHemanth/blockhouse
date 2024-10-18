import pandas as pd
from .models import *
from .serivces import *
import tempfile
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt


def generate_report(symbol, initial_investment):
    
    
    actual_data = stockPricesData.objects.filter(symbol=symbol, type='A').order_by('-date')[:30].values('date', 'close_price')

    if not actual_data:
        actual_data=fetch_stock_data(symbol)
    if not actual_data:
        raise StockDataError("No data")

    actual_df = pd.DataFrame(list(actual_data))

    actual_df['date'] = pd.to_datetime(actual_df['date'])

    predictions_data = stockPricesData.objects.filter(symbol=symbol, type='P').order_by('-date')[:30].values('date', 'close_price')

    if not predictions_data:
        predict_next_30_days_and_store(symbol)
    if not predictions_data:
        raise StockDataError("No data")

    predictions_df = pd.DataFrame(list(predictions_data))

    predictions_df['date'] = pd.to_datetime(predictions_df['date'])

   
    backtest_results = backtest_strategy(symbol, int(initial_investment))

    # predicted vs actual prices

    plt.figure(figsize=(10, 6))
    plt.plot(actual_df['date'], actual_df['close_price'], label='Actual Prices', color='blue', marker='o')
    plt.plot(predictions_df['date'], predictions_df['close_price'], label='Predicted Prices', color='orange', marker='x')
    plt.title(f'Stock Price Predictions vs Actual for {symbol} (Last 30 Days vs future 30 days)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()

    

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    #backtesting metrics report
    report_json = {
        "symbol": symbol,
        "backtest_metrics": backtest_results,  
        'predictions': predictions_data,
        'actuals': actual_data,
    }

    plt.close()

    return report_json, buf


def create_pdf_report(symbol, initial_investment):

    report_json, plot_buf = generate_report(symbol, initial_investment)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{symbol}_report.pdf"'

    pdf_buffer = BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=letter)

    pdf_canvas.drawString(100, 750, f"Stock Report for {symbol}")
    pdf_canvas.drawString(100, 730, f"Backtest Metrics:")
    
    y_position = 710
    for metric, value in report_json['backtest_metrics'].items():
        pdf_canvas.drawString(100, y_position, f"{metric}: {value}")
        y_position -= 20

   
    with tempfile.NamedTemporaryFile(delete=True, suffix=".png") as temp_file:
        temp_file.write(plot_buf.getvalue())
        temp_file.flush() 
        pdf_canvas.drawImage(temp_file.name, 50, 300, width=500, height=300)

    

    pdf_canvas.showPage()
    pdf_canvas.save()

    pdf_buffer.seek(0)
    response.write(pdf_buffer.read())

    return response

