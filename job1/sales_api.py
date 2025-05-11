"""
Логика первой джобы: загрузка данных о продажах из внешнего API и сохранение в JSON.
"""

import os
import json
import requests


AUTH_TOKEN = os.environ.get('AUTH_TOKEN')  # Токен должен быть в окружении


def fetch_sales_data(date: str) -> list:
    """
    Загружает данные о продажах по страницам для указанной даты.
    """
    api_url = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"
    headers = {"Authorization": AUTH_TOKEN} if AUTH_TOKEN else {}

    all_data = []
    page = 1

    while True:
        try:
            response = requests.get(
                api_url,
                params={"date": date, "page": page},
                headers=headers
            )
            if response.status_code == 404:
                break  # Больше данных нет

            response.raise_for_status()
            data = response.json()

            if not data:
                break

            all_data.extend(data)
            page += 1

        except requests.exceptions.HTTPError as e:
            print(f"Ошибка на странице {page}: {e}")
            break

    return all_data


def save_sales_data(date: str, raw_dir: str, data: list) -> str:
    """
    Сохраняет полученные данные в файл JSON по пути: raw_dir/sales/{date}/sales_{date}.json
    """
    save_dir = os.path.join(raw_dir, "sales", date)
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, f"sales_{date}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return file_path
