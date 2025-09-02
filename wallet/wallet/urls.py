"""
URL configuration for app_rest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path

from .views import AsyncWalletView, WalletView

urlpatterns = [
    path('<uuid:id>/', AsyncWalletView.as_view(), name='balance_check'),                        #async
    path('<uuid:id>/operation/', AsyncWalletView.as_view(), name='operation'),                              #async
]
