import requests

url = "https://www.okx.com/api/v5/market/tickers?instType=SWAP"
response = requests.get(url)

# Проверяем статус ответа
if response.status_code == 200:
    # Получаем текущий курс обмена USD/RUB
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response_rub = requests.get(url)
    data_rub = response_rub.json()
    usd_to_rub = data_rub['rates']['RUB']

    data = response.json()
    prices = [(float(item['last']), item['instId']) for item in data['data']]
    prices_in_rub = [(price * usd_to_rub, instId) for price, instId in prices]
    min_price, min_instId = min(prices_in_rub, key=lambda x: x[0])
    max_price, max_instId = max(prices_in_rub, key=lambda x: x[0])
    min_instId = min_instId.split('-')[0]
    max_instId = max_instId.split('-')[0]

    min_price = "{:.8f}".format(min_price)

else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")

