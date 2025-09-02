from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
from django.test import Client
from .models import Wallet
# from .views import WalletView
from .views import AsyncWalletView                  #async

import decimal

# Тестирование DRF через APIRequestFactory
# class WalletViewTests(TestCase):
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.wallet_1 = Wallet.objects.create(account=13)
#         self.wallet_2 = Wallet.objects.create(account=37)
#
#     def test_get(self):
#         url = reverse("balance_check", kwargs={'id': self.wallet_1.pk})
#         request = self.factory.get(url)
#         view = WalletView.as_view()
#         response = view(request, id=self.wallet_1.pk)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["account"], '13.00')
#
#     def test_post(self):
#         url = reverse("operation", kwargs={"id": self.wallet_1.pk})
#         data = {"amount": 1300, "operation_type": "DEPOSIT"}
#         request = self.factory.post(url, data, format="json")
#         view = WalletView.as_view()
#         response = view(request, id=self.wallet_1.pk)
#         update_wallet_1 = (Wallet.objects.get(pk=self.wallet_1.pk))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(update_wallet_1.account, 1313)


# Тестирование DRF через APIClient
# class WalletViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.wallet_1 = Wallet.objects.create(account=13)
#         self.wallet_2 = Wallet.objects.create(account=37)
#
#     def test_get(self):
#         url = reverse("balance_check", kwargs={'id': self.wallet_1.pk})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["account"], '13.00')
#
#         def test_post(self):
#             url = reverse("operation", kwargs={"id": self.wallet_1.pk})
#             data = {"amount": 1300, "operation_type": "DEPOSIT"}
#             response = self.clietn.get(url)
#             update_wallet_1 = Wallet.objects.get(pk=self.wallet_1.pk)
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.assertEqual(update_wallet_1.account, 1313)


# Тестирвоние Django. Использование БД в unittest фреймворка Django

class WalletView(TestCase):
    fixtures = ['wallet_wallet.json']

    def test_get(self):
        w = Wallet.objects.all()
        path = reverse('balance_check', kwargs={"id": w[2].pk})
        response = self.client.get(path)
        self.assertEqual(response.data["account"], "52.52")

    def test_post_deposit(self):
        all_w = Wallet.objects.all()
        w = all_w[0]
        new_account = w.account + 100
        path = reverse("operation", kwargs={"id": w.pk})
        response = self.client.post(path, data={"amount": 100, "operation_type": "DEPOSIT"})
        new_w = Wallet.objects.get(id=w.pk)
        self.assertEqual(response.data, {"message": "Balance has changed successfully!"})
        self.assertEqual(new_account, new_w.account)

    def test_post_not_enough_founds(self):
        w = Wallet.objects.all()
        path = reverse('operation', kwargs={"id": w[2].pk})
        response = self.client.post(path, data={"amount": 100, "operation_type": "WITHDRAW"})
        self.assertEqual(response.data, {"message":"insufficient funds"})

    def test_post_too_big_amount(self):
        all_w = Wallet.objects.all()
        w = all_w[0]
        path = reverse('operation', kwargs={"id": w.pk}) #start = 100
        response = self.client.post(path, data={"amount": decimal.Decimal(10**50), "operation_type": "DEPOSIT"})
        self.assertEqual(response.data, {"message": "Bad data!"})

    # def test_concurrent_withdraw(self):
    #     import threading
    #     lock = threading.Lock()
    #     responses_data = []
    #     threads = []
    #     all_w = Wallet.objects.all()
    #     w = all_w[0]
    #     # w = Wallet.objects.filter(account=decimal.Decimal(300)).first()
    #     path = reverse("operation", kwargs={"id": w.pk})
    #     def withdraw(path, amount):
    #         response = self.client.post(path, data={"amount": amount, "operation_type": "WITHDRAW"})
    #         # if response.status_code == 200:
    #         lock.acquire()
    #         try:
    #             responses_data.append(response.data)
    #         finally:
    #             lock.release()
    #         print(responses_data)
    #     all_w = Wallet.objects.all()
    #     for i in range(len(all_w)):
    #         thread = threading.Thread(target=withdraw, kwargs={"path": path, "amount": 100*i})
    #         threads.append(thread)
    #         thread.start()
    #
    #     for thread in threads:
    #         thread.join()
    #
    #     self.assertEqual(True, {"message": "insufficient funds"} in responses_data)
    #     self.assertEqual(True, responses_data.count({'message': 'Balance has changed successfully!'})==2)

    # def test_concurrent_withdraw(self):
    #     import threading
    #     from concurrent.futures import ThreadPoolExecutor
    #
    #     # Создаем кошелек с конкретным балансом
    #     wallet = Wallet.objects.create(account=decimal.Decimal('300.00'))
    #     path = reverse("operation", kwargs={"id": wallet.pk})
    #
    #     responses_data = []
    #     lock = threading.Lock()
    #
    #     def make_withdraw(amount):
    #         # Каждый поток делает запрос на снятие
    #         client = Client()
    #         response = client.post(path, {
    #             "amount": str(amount),
    #             "operation_type": "WITHDRAW"
    #         })
    #         with lock:
    #             responses_data.append(response.data)
    #         return response
    #
    #     # Создаем несколько запросов на снятие
    #     amounts = [100, 200, 150, 400]  # Суммы для снятия
    #
    #     # Используем ThreadPoolExecutor для управления потоками
    #     with ThreadPoolExecutor(max_workers=4) as executor:
    #         results = list(executor.map(make_withdraw, amounts))
    #
    #     # Обновляем данные кошелька из БД
    #     wallet.refresh_from_db()
    #
    #     # Анализируем результаты
    #     success_count = sum(1 for r in responses_data
    #                         if r.get('message') == 'Balance has changed successfully!')
    #
    #     insufficient_count = sum(1 for r in responses_data
    #                              if r.get('message') == 'insufficient funds')
    #
    #     print(f"Успешных операций: {success_count}")
    #     print(f"Отказов: {insufficient_count}")
    #     print(f"Финальный баланс: {wallet.account}")
    #
    #     # Проверяем логику
    #     self.assertEqual(success_count + insufficient_count, len(amounts))
    #     self.assertTrue(insufficient_count > 0)  # Должны быть отказы
    #     self.assertEqual(wallet.account, decimal.Decimal('0.00'))  # 300 - 100 - 200 = 0

    def test_concurrent_withdraw_diagnostic(self):
        import threading
        from django.test import Client

        responses_data = []
        threads = []

        # Создаем отдельный клиент для КАЖДОГО потока
        def make_request(thread_id):
            try:
                client = Client()  # Отдельный клиент для каждого потока
                response = client.post(
                    reverse("operation", kwargs={"id": self.wallet.pk}),
                    data={"amount": 100, "operation_type": "WITHDRAW"}
                )
                responses_data.append(response.data)
                print(f"Thread {thread_id}: {response.status_code}")
            except Exception as e:
                print(f"Thread {thread_id} failed: {e}")
                responses_data.append({"error": str(e)})

        for i in range(4):
            thread = threading.Thread(target=make_request, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print(f"All responses: {responses_data}")