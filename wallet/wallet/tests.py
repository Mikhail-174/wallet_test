from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status

from .models import Wallet
from .views import WalletView

import decimal
# Create your tests here.

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

    def test_post_not_enough_founds(self):
        w = Wallet.objects.all()
        path = reverse('operation', kwargs={"id": w[2].pk})
        response = self.client.post(path, data={"amount": 100, "operation_type": "WITHDRAW"})
        self.assertEqual(response.data, {"message":"insufficient funds"})

    def test_post_too_big_amount(self):
        w = Wallet.objects.all()
        path = reverse('operation', kwargs={"id": w[0].pk}) #start = 100
        response = self.client.post(path, data={"amount": decimal.Decimal(10**50), "operation_type": "DEPOSIT"})
        self.assertEqual(response.data, {"message": "Bad data!"})

    def test_concurrent_withdraw(self):
        import threading
        responses_data = []
        threads = []
        w = Wallet.objects.all()[4]
        path = reverse("operation", kwargs={"id": w.pk})
        def withdraw(path, amount):
            response = self.client.post(path, data={"amount": amount, "operation_type": "WITHDRAW"})
            if response.status_code == 200:
                responses_data.append(response.data)

        for i in range(1, 4):
            thread = threading.Thread(target=withdraw, kwargs={"path": path, "amount": 100*i})
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(True, {"message":"insufficient funds"} in responses_data)
        self.assertEqual(True, responses_data.count({'message': 'Balance has changed successfully!'})==2)


