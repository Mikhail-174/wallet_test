from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
from .models import Wallet
# from .views import WalletView, AsyncWalletView

import decimal

# Тестирование DRF через APIRequestFactory
# class WalletViewTest(TestCase):
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


class WalletViewTest(TestCase):
    fixtures = ['wallet_wallet.json']

    def test_get(self):
        all_w = Wallet.objects.all()
        w = all_w[2]
        path = reverse('balance_check', kwargs={"id": w.pk})
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
        all_w = Wallet.objects.all()
        w = all_w[2]
        path = reverse('operation', kwargs={"id": w.pk})
        response = self.client.post(path, data={"amount": 100, "operation_type": "WITHDRAW"})
        self.assertEqual(response.data, {"message":"insufficient funds"})

    def test_post_too_big_amount(self):
        all_w = Wallet.objects.all()
        w = all_w[0]
        path = reverse('operation', kwargs={"id": w.pk}) #start = 100
        response = self.client.post(path, data={"amount": decimal.Decimal(10**50), "operation_type": "DEPOSIT"})
        self.assertEqual(response.data, {"message": "Bad data!"})

    # не работает пока что... Параллелизм тестировать через внешнюю прогу sender.py
    # def test_concurrent_withdraw(self):
    #     from rest_framework.test import APIClient
    #     import threading
    #     lock = threading.Lock()
    #     responses_data, threads = [], []
    #     all_w = Wallet.objects.all()
    #     w = all_w[4]
    #     path = reverse("operation", kwargs={"id": w.pk})
    #
    #     def withdraw(amount):
    #         client = APIClient()
    #         response = client.post(path, data={"amount": amount, "operation_type": "WITHDRAW"})
    #         lock.acquire()
    #         try:
    #             responses_data.append(response.data)
    #         finally:
    #             lock.release()
    #         print(responses_data)
    #
    #     for i in range(4):
    #         thread = threading.Thread(target=withdraw, kwargs={"amount": 100})
    #         threads.append(thread)
    #         thread.start()
    #
    #     for thread in threads:
    #         thread.join()
    #
    #     self.assertEqual(True, {"message": "insufficient funds"} in responses_data)
    #     self.assertEqual(True, responses_data.count({'message': 'Balance has changed successfully!'})==3)