import decimal

from django.shortcuts import render
from django.db import models

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WalletSerializer
from .models import Wallet
import decimal

# Create your views here.
class WalletView(APIView):
    serializer_class = WalletSerializer


    def get_object(self, id):
        try:
            wallet = Wallet.objects.get(id=id)
            return wallet
        except Wallet.DoesNotExist:
            return Response(data={"message": "Wallet does not exist!"}, status=404)

    # detail = True / False: Указывает, нужно ли использовать идентификатор (PK) ресурса в URL. Но я как бы и так прописываю в urls, что по UUID строится маршрут... Так что detail=True/False не влияет
    @action(methods=['post'], detail=False)
    def post(self, request, *args, **kwargs):
        operation = request.data.get('operation_type')
        amount = decimal.Decimal(request.data.get('amount'))
        wallet = self.get_object(kwargs['id'])
        new_wallet = None
        if operation.upper() not in ('WITHDRAW', 'DEPOSIT'):
            return Response(data={"message": "No operation in request "}, status=400)

        if operation.upper()=='WITHDRAW':
            if (wallet.account - amount) >= 0:
                new_wallet = wallet.account - amount
            else:
                return Response(data={"message": "insufficient funds"}, status=400)

        if operation.upper()=='DEPOSIT':
            new_wallet = wallet.account + amount

        if not self.serializer_class(data={"account": new_wallet}).is_valid():
            return Response(data={"message": "Bad data!"}, status=400)

        wallet.account = new_wallet
        wallet.save()
        return Response(data={"message": "Balance has changed successfully!"}, status=200)

    @action(methods=['get'], detail=False)
    def get(self, request, *args, **kwargs):
        wallet = self.get_object(kwargs['id'])
        serializer = self.serializer_class(wallet)
        return Response(data=serializer.data, status=200)


