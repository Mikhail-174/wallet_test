import requests
import threading
import time


WALLET_UUID = "a058aaca-e0a7-4edf-8ea9-149dffe54ac6"
url_get = f"http://localhost:8000/api/v1/wallets/{WALLET_UUID}"
url_post = f"http://localhost:8000/api/v1/wallets/{WALLET_UUID}/operation"

wallet_uuids = ["d15a7be2-a042-4968-9a78-259cae566076",
            "59cfa93c-4bec-483a-872a-f7e2bf0fdc36",
            "ed0802cf-056f-4d51-b5b9-791b95947743",
            "602dd697-6e2b-4af9-a77c-e1c07fd4f84d",
            "2ed5ef74-9066-4931-a86a-33579828e89d",
]
urls_for_sync = [
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[0]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[0]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[0]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[0]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[0]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[0]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[0]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[0]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[0]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[1]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[2]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[3]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[3]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[3]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[3]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[3]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[3]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[3]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[3]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}",
]

urls_for_concurrent = [
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}/operation/",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}/operation/",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}/operation/",
    f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}/operation/",
]

def deposit(url):
    try:
        start_time = time.time()
        response = requests.post(url, data={"amount": 100, "operation_type": "WITHDRAW"})
        duration = time.time() - start_time
        print(f"Загружен {url[:52]}.. за {duration: .2f} сек. Статус: {response.status_code} ")
        print(response)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке {url}: {e}")

# многопоточно
threads = list()
for url in urls_for_concurrent:
    thread = threading.Thread(target=deposit, args=(url,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

try:
    response = requests.get(f"http://localhost:8000/api/v1/wallets/{wallet_uuids[4]}")
    print(f"Status Code: {response.status_code}. Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("Ошибка подключения. Убедитесь, что сервер запущен на localhost:8000")
except Exception as e:
    print(f"Произошла ошибка: {e}")

# по порядку
# try:
#     for url in urls_for_sync:
#         response = requests.get(url)
#
#         print(f"Status Code: {response.status_code}")
#         print(f"Response: {response.json()}")
#
# except requests.exceptions.ConnectionError:
#     print("Ошибка подключения. Убедитесь, что сервер запущен на localhost:8000")
# except Exception as e:
#     print(f"Произошла ошибка: {e}")