import requests
import datetime as dt
import time
import random

#Uses the Alpha Vantage API to fetch data from the ticker symbol.
def Stock_info(ticker):
    Api_Key = "00BLEDRGCXSGA8WG"  
    interval = "5min" #Stock Prices updated every 5
    date = dt.datetime.now()

    time.sleep(random.uniform(2, 6))

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}&apikey={Api_Key}"

    response = requests.get(url)
    data = response.json()

    # Get the latest stock price
    latest_time = list(data["Time Series (5min)"].keys())[0]
    latest_price = data["Time Series (5min)"][latest_time]["1. open"]

    #Store the information on the ticker. price and date within a txt file.
    with open("Purchased_stock.txt", "a", encoding="utf-8") as f:
        f.write("\n")
        f.write(f"Purchased stock: {ticker}, Value: ${latest_price}, Date: {date}")
    
    if ticker != None:
        return True