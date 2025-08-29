import requests
import threading
import time


WALLET_UUID = "a058aaca-e0a7-4edf-8ea9-149dffe54ac6"
url_get = f"http://localhost:8000/api/v1/wallets/{WALLET_UUID}"
url_post = f"http://localhost:8000/api/v1/wallets/{WALLET_UUID}/operation"

wallet_uuids = ["a058aaca-e0a7-4edf-8ea9-149dffe54ac6",
            "ac242451-cf2e-437d-bda2-905825406b27",
            "f828c13e-a976-48ed-a0ec-3286c4eb4585",
            "7cab6001-74d7-4937-8b9b-b2f7da9060f8",
            "2c0cea8c-7d88-4f5d-85a2-f1ab0c7de0f3",
]
urls = [
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
def fetch_url(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        duration = time.time() - start_time
        print(f"Загружен {url} за {duration: .2f} сек. Статус: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке {url}: {e}")



# в многопоточно
threads = list()
for url in urls:
    thread = threading.Thread(target=fetch_url, args=(url,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()



# по порядку
try:
    for url in urls:
        response = requests.get(url)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

except requests.exceptions.ConnectionError:
    print("Ошибка подключения. Убедитесь, что сервер запущен на localhost:8000")
except Exception as e:
    print(f"Произошла ошибка: {e}")