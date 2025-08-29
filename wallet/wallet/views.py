from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from serializers import WalletSerializer
from .models import Wallet

# Create your views here.
class WalletOperationView(APIView):
    serializer_class = WalletSerializer
    def post(self, request, *args, **kwargs):
        operation = request.GET.get('operation_type')
        amount = int(request.GET.get('amount'))
        wallet = Wallet.objects.get(id=kwargs['id'])
        if operation.upper()=='WITHDROW':
            print(operation, amount)
            pass
        if operation.upper()=='DEPOSIT':
            print(operation, amount)
            pass

