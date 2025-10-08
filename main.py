import os, json, requests, pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import yfinance as yf

# Google Sheets Auth
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

sheet = client.open("Memecoin Tracker").sheet1

# Config Telegram
bot_token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram_alert(msg):
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}")

# Função exemplo CoinGecko
def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids":"dogecoin,shiba-inu","vs_currencies":"usd","include_24hr_change":"true"}
    r = requests.get(url, params=params).json()
    return r

# Função para obter preços de ações via Yahoo Finance
def get_stock_prices():
    stocks = ["PETR4.SA"]  # Petrobras
    stock_data = {}
    
    for symbol in stocks:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")  # últimos 2 dias
            
            if len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                previous_price = hist['Close'].iloc[-2]
                change = ((current_price - previous_price) / previous_price) * 100
                
                stock_data[symbol] = {
                    "usd": current_price,
                    "usd_24h_change": change
                }
        except Exception as e:
            print(f"Erro ao obter dados de {symbol}: {e}")
    
    return stock_data

def save_price(coin, price, change):
    sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), coin, price, change])

THRESHOLD = 1

# Rastrear memecoins
data = get_prices()
for coin, info in data.items():
    price, change = info["usd"], info["usd_24h_change"]
    save_price(coin, price, change)
    if abs(change) >= THRESHOLD:
        send_telegram_alert(f"⚡ {coin} mudou {change:.2f}% nas últimas 24h!")

# Rastrear ações
stock_data = get_stock_prices()
for stock, info in stock_data.items():
    price, change = info["usd"], info["usd_24h_change"]
    save_price(stock, price, change)
    if abs(change) >= THRESHOLD:
        send_telegram_alert(f"📈 {stock} mudou {change:.2f}% nas últimas 24h!")

