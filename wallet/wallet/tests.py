from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status

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
        print(w)
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

    def test_concurrent_withdraw(self):
        import threading
        lock = threading.Lock()
        responses_data = []
        threads = []
        w = Wallet.objects.filter(account=decimal.Decimal(300)).first()
        path = reverse("operation", kwargs={"id": w.pk})
        def withdraw(path, amount):
            response = self.client.post(path, data={"amount": amount, "operation_type": "WITHDRAW"})
            # if response.status_code == 200:
            lock.acquire()
            try:
                responses_data.append(response.data)
            finally:
                lock.release()
            print(responses_data, "BUBA")
        all_w = Wallet.objects.all()
        for i in range(len(all_w)):
            thread = threading.Thread(target=withdraw, kwargs={"path": path, "amount": 100*i})
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(True, {"message": "insufficient funds"} in responses_data)
        self.assertEqual(True, responses_data.count({'message': 'Balance has changed successfully!'})==2)

    # def test_concurrent_withdraw(self):
    #     from concurrent.futures import ThreadPoolExecutor
    #     from django.db import connection
    #
    #     # Закрываем соединение, чтобы каждому потоку создать свое
    #     connection.close()
    #     all_w = Wallet.objects.all()
    #     w = Wallet.objects.get(id=all_w[0].pk)
    #     initial_balance = w.balance
    #     path = reverse("operation", kwargs={"id": w.pk})
    #
    #     def make_withdraw(amount):
    #         # Создаем отдельный клиент для каждого потока
    #         from django.test import Client
    #         client = Client()
    #         return client.post(path, {
    #             "amount": amount,
    #             "operation_type": "WITHDRAW"
    #         })
    #
    #     amounts = [100 * i for i in range(5)]
    #     responses_data = []
    #
    #     with ThreadPoolExecutor(max_workers=5) as executor:
    #         results = executor.map(make_withdraw, amounts)
    #         responses_data = list(results)
    #
    #     # Проверяем результаты
    #     success_count = sum(1 for r in responses_data
    #                         if r.status_code == 200 and
    #                         r.data.get('message') == 'Balance has changed successfully!')
    #
    #     insufficient_count = sum(1 for r in responses_data
    #                              if r.status_code == 400 and
    #                              r.data.get('message') == 'insufficient funds')
    #
    #     # Обновляем объект из базы
    #     w.refresh_from_db()
    #
    #     # Проверяем, что баланс изменился корректно
    #     expected_final_balance = initial_balance - sum(amount for amount in amounts
    #                                                    if amount <= initial_balance)
    #
    #     self.assertEqual(w.balance, expected_final_balance)
    #     self.assertEqual(success_count + insufficient_count, len(amounts))

