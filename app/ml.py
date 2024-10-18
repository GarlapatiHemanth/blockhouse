from sklearn.linear_model import LinearRegression
import pickle
import pandas as pd

def trainmodel(data):

    
    df = list(data.values('date', 'close_price'))
    df = pd.DataFrame(df)
    
    df['date_ordinal'] = pd.to_datetime(df['date']).map(pd.Timestamp.toordinal)
    
    
    X = df['date_ordinal'].values.reshape(-1, 1)  
    y = df['close_price'].values  

 
    model = LinearRegression()
    model.fit(X, y)
    
    with open('linear_regression_model.pkl', 'wb') as file:
        pickle.dump(model, file)
    
    print("Model trained and saved as linear_regression_model.pkl")
