import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from sklearn.ensemble import RandomForestRegressor
from pandas_datareader import data


def get_stock_info(stock_name,day): #getting stock info
    try:
        end_date=str(datetime.now()).split()[0]
        start_date=str(datetime.now()-timedelta(days=day)).split()[0]
        df = data.DataReader(stock_name, 'yahoo', start_date, end_date)
        return df
    except Exception as err:
        print("An Error Occured.Please Try Again Later.")
        print("Please Check Stock Name")
        print(err)

def predict(stock_name,day,day_later,queue1,queue2):
    data=get_stock_info(stock_name,day)
    value=data.iloc[-1:,queue1:queue2].astype(float).values[0][0]
    use_value=data.iloc[day_later:,queue1:queue2]
    data=data.shift(periods=day_later)#The data is shifted by the specified value .The next data is predicted.
    X=use_value.astype(float).values
    Y=data.iloc[day_later:,queue1:queue2].astype(float).values
    rf_reg=RandomForestRegressor(n_estimators=10,random_state=0)#using random forest to predict
    rf_reg.fit(X,Y)
    return rf_reg.predict([[value]])

def list_max_min(stock_name,day,day_later,queue1,queue2):
    data=get_stock_info(stock_name,day)
    maxi=0
    maxi_day=0
    mini=999999999999
    mini_day=0
    c=data #we use this because we shifted the data so we should use main data
    for i in range(day_later):
        later=i #Number of data to shift
        value=data.iloc[-1:,queue1:queue2].astype(float).values[0][0]
        use_value=data.iloc[i:,queue1:queue2]
        data=data.shift(periods=i) 
        X=use_value.astype(float).values
        Y=data.iloc[i:,queue1:queue2].astype(float).values
        rf_reg=RandomForestRegressor(n_estimators=10,random_state=0)
        rf_reg.fit(X,Y)
        predict=rf_reg.predict([[value]])
        if  predict>maxi:
            maxi=predict
            maxi_day=i 
        if predict<mini:
            mini=predict
            mini_day=i
        data=c
    
    return maxi_day,maxi,mini_day,mini

def determine_queue(column_name):
    queue1=0
    queue2=1
    if column_name=="high":
        queue1=0
        queue2=1
    elif column_name=="low":
        queue1=1
        queue2=2
    elif column_name=="open":
        queue1=2
        queue2=3
    elif column_name=="close":
        queue1=3
        queue2=4
    return queue1,queue2


while True:
    option=input("1-Predict to Day\n2-Predict Max and Min\n3-Exit\nYour Choice:")
    if option=="1":
        try:
            stock_name=input("Please Enter Stock Name:")
            column_name=input("Please Enter Data Name to Use(High/Low/Open/Close):")
            day=int(input("Data Start Time (in Days) for Evaluation to be Used:"))
            day_later=int(input("After How Many Days:"))
            queue1,queue2=determine_queue(column_name.lower())
            result=predict(stock_name.upper(),day,day_later,queue1,queue2)
            print(f"Result:{result}")
        except Exception as err:
            print("Please enter the required information correctly and try again.")
            print(err)
            
    elif option=="2":
        try:
            stock_name=input("Please Enter Stock Name:")
            column_name=input("Please Enter Data Name to Use(High/Low/Open/Close):")
            day=int(input("Data Start Time (in Days) for Evaluation to be Used:"))
            day_later=int(input("After How Many Days:"))
            queue1,queue2=determine_queue(column_name.lower())
            maxi_day,maxi,mini_day,mini=list_max_min(stock_name.upper(),day,day_later,queue1,queue2)
            print("Maksimum".center(100,"-"))
            print(f"Day:{maxi_day} Value:{maxi}")
            print("Minimum".center(100,"-"))
            print(f"Day:{mini_day} Value:{mini}")            
                             
        except Exception as err:
            print("Please enter the required information correctly and try again.")
            print(err)
            
    elif option=="3":
        print("Exit Succesfully")
        break     
    
    else:
        print("Please Enter Value Between 1-3 and Try Again.")








