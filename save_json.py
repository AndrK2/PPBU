import requests
import json



# Получаем данные по USD
r = requests.get('https://open.er-api.com/v6/latest/USD')
data = r.json()

# Сохраняем в файл
with open('currencies.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Файл currencies.json сохранён!")
print(f"Валют: {len(data['rates'])}")
print(f"Базовая валюта: {data['base_code']}")
print(f"Последнее обновление: {data['time_last_update_utc']}")
