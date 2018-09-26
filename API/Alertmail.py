from flask import Flask
import requests
from flask_mail import Mail, Message

def checkalert():
    url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/latest?period_id=1MIN&limit=1'
    headers = {'X-CoinAPI-Key' : '383632BE-23C4-4ECA-B54E-4056D1BA597E'}
    response = requests.get(url, headers=headers)
    data = (response.json()[0]['price_close'])
    print (data)
 









