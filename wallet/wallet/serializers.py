from rest_framework import serializers
from .models import Wallet

# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'