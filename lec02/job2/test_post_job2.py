"""
Тестовая отправка запроса на вторую джобу (конвертация JSON → Avro).
"""

import requests

# URL второй джобы (Flask-сервер job2 должен быть запущен на порту 8082)
url = "http://127.0.0.1:8082/convert"

# Параметры запроса (пути к raw и stg директориям)
data = {
    "raw_dir": "file_storage/raw/sales/2022-08-10",
    "stg_dir": "file_storage/stg/sales/2022-08-10"
}

# Отправка POST-запроса
response = requests.post(url, json=data)

# Вывод результата
print("Status code:", response.status_code)
print("Response:", response.json())
