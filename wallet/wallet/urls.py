"""
URL configuration for app_rest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from .views import

urlpatterns = [
    path('<uuid:id>/operation/', ),
    path('<uuid:id>/'),
]
