THRESHOLD = 1  # % de variação para alertas

data = get_prices(COINS)

for coin, info in data.items():
    price = info['usd']
    change = info['usd_24h_change']
    save_price(coin, price, change)
    if abs(change) >= THRESHOLD:
        send_telegram_alert(f"⚡ {coin} mudou {change:.2f}% nas últimas 24h!")
