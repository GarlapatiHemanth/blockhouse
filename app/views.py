from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serivces import *
from .serializers import *
from .reports import *

# Create your views here.
        

@api_view(['GET'])
def fetch_data(request):
    symbol=request.GET.get('symbol')
    if not symbol:
        return Response("Symbol is required",400)
    try:
        data=fetch_stock_data(request.GET.get('symbol').upper())

        return Response(stockPricesDataSerializers(data,many=True).data)
    except Exception as e:
        print(e)
        return Response("Internal server error",status=400)

@api_view(['POST'])
def run_backtest(request):
    symbol = request.data.get('symbol')
    initial_investment = request.data.get('initial_investment')
    
    try:
        result = backtest_strategy(symbol.upper(), initial_investment)
        return Response(result)
    except Exception as e:
        return Response("Internal Error Occured", status=400)
    
@api_view(['GET'])
def predict_stock_prices(request):

    try:
        symbol=request.GET.get('symbol')
        if not symbol:
            return Response("Symbol is required",400)
        predictions = predict_next_30_days_and_store(symbol.upper())
        return Response(predictions.to_dict(orient='records'))
    except Exception as e:
        print(e)
        return Response("Internal Error Occured", status=400)

@api_view(['GET'])
def report(request):

    symbol=request.GET.get('symbol')
    initialInvestment=request.GET.get('initialInvestment')
    

    if not symbol:
        return Response("Symbol is required",400)
    
    if not initialInvestment:
        return Response("Initial Investment is required",400)
    try:
        if request.GET.get('f') =='pdf':
         
            return create_pdf_report(symbol.upper(),initialInvestment)
        else:  
            return Response(generate_report(symbol.upper(),initialInvestment)[0])
    except Exception as e:
        print(e)
        return Response('Internal Server Error',status=400)
    


    
   
