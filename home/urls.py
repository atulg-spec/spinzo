# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home', views.index, name='index'),
    path('add-funds', views.addFunds, name='addFunds'),
    path("razorpay-check-status/",views.razorpay_payment_status,name='razorpay_payment_status'),
    path('transactions', views.transactions, name='transactions'),
    path('my-account', views.my_account, name='my_account'),
]