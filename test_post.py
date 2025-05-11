import requests

url = "http://localhost:8081"

data = {
    "date": "2022-08-10",
    "raw_dir": "file_storage/raw/sales/2022-08-10"
}


response = requests.post(url, json=data)
print("Status code:", response.status_code)
print("Response:", response.json())
