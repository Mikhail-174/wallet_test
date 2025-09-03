from django.shortcuts import render
from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from .serializers import WalletSerializer
from .models import Wallet
import decimal


class WalletView(APIView):
    serializer_class = WalletSerializer

    def get_object(self, id):
        try:
            wallet = Wallet.objects.get(id=id)
            return wallet
        except Wallet.DoesNotExist:
            return None

    # обязательный detail = True/False: Указывает, нужно ли использовать идентификатор (PK) ресурса в URL.
    @action(methods=['post'], detail=False)
    def post(self, request, *args, **kwargs):
        from django.db import transaction

        with transaction.atomic():
            operation = request.data.get('operation_type')
            amount = decimal.Decimal(request.data.get('amount'))
            wallet =  Wallet.objects.select_for_update().get(id=kwargs['id'])

            if operation.upper() not in ('WITHDRAW', 'DEPOSIT'):
                return Response(data={"message": "No operation in request "}, status=400)

            if operation.upper()=='WITHDRAW':
                if (wallet.account - amount) >= 0:
                    wallet.account -= amount
                else:
                    return Response(data={"message": "insufficient funds"}, status=400)

            if operation.upper()=='DEPOSIT':
                wallet.account += amount

            if not self.serializer_class(data={"account": wallet.account}).is_valid():
                return Response(data={"message": "Bad data!"}, status=400)
            wallet.save()
            return Response(data={"message": "Balance has changed successfully!"}, status=200)

    @action(methods=['get'], detail=False)
    def get(self, request, *args, **kwargs):
        wallet = self.get_object(kwargs['id'])

        if wallet is None:
            return Response(data={"message": "Bad data!"}, status=400)

        serializer = self.serializer_class(wallet)
        return Response(data=serializer.data, status=200)

#async class
from adrf.views import APIView
from asgiref.sync import sync_to_async
from .serializers import AsyncWalletSerializer

class AsyncWalletView(APIView):
    serializer_class = AsyncWalletSerializer

    async def get_object(self, id):
        try:
            wallet = await Wallet.objects.aget(id=id)
            return wallet
        except Wallet.DoesNotExist:
            return None

    async def post(self, request, *args, **kwargs):
        operation = request.data.get('operation_type')
        amount = decimal.Decimal(request.data.get('amount'))
        wallet = await Wallet.objects.aget(id=kwargs['id'])

        if wallet is None:
            return Response(data={"message": "Bad data!"}, status=400)

        if operation.upper() not in ('WITHDRAW', 'DEPOSIT'):
            return Response(data={"message": "No operation in request "}, status=400)

        if operation.upper()=='WITHDRAW':
            if (wallet.account >= amount):
                wallet.account -= amount
            else:
                return Response(data={"message": "insufficient funds"}, status=400)

        if operation.upper()=='DEPOSIT':
            wallet.account += amount

        serializer = self.serializer_class(data={"account": wallet.account})
        if not serializer.is_valid():
            return Response(data={"message": "Bad data!"}, status=400)

        await wallet.asave()
        serializer = self.serializer_class(wallet)
        return Response(data=serializer.data, status=200)


    async def get(self, request, *args, **kwargs):
        wallet = await self.get_object(kwargs['id'])
        if wallet is None:
            return Response(data={"message": "Bad data!"}, status=400)
        serializer = self.serializer_class(wallet)
        return Response(data=serializer.data, status=200)
