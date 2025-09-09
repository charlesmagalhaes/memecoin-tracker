import os, json, requests, pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

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

def save_price(coin, price, change):
    sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), coin, price, change])

THRESHOLD = 1

data = get_prices()
for coin, info in data.items():
    price, change = info["usd"], info["usd_24h_change"]
    save_price(coin, price, change)
    if abs(change) >= THRESHOLD:
        send_telegram_alert(f"⚡ {coin} mudou {change:.2f}% nas últimas 24h!")

