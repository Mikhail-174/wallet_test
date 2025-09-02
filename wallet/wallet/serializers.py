from rest_framework import serializers
from .models import Wallet

# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'




# Асинхронный код
from adrf.serializers import Serializer

class AsyncWalletSerializer(Serializer):
    account = serializers.DecimalField(max_digits=52, decimal_places=2)
