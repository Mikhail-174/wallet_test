import decimal

from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WalletSerializer
from .models import Wallet
from django.db import models
import decimal

# Create your views here.
class WalletView(APIView):
    serializer_class = WalletSerializer


    def get_object(self, id):
        try:
            wallet = Wallet.objects.get(id=id)
            return wallet
        except models.Model.DoesNotExist:
            return Response(data={"message": "Wallet does not exist!"}, status=404)

    @action(methods=['post'], detail=True)
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
        return Response(data={"message": "Balance has changed successfully!"}, status=201)

    @action(methods=['get'], detail=True)
    def get(self, request, *args, **kwargs):
        wallet = self.get_object(kwargs['id'])
        serializer = self.serializer_class(wallet)
        return Response(data=serializer.data, status=200)


