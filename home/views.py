import json
from .models import *
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import csv
from app.models import GatewaySettings, PaymentSettings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.utils.dateparse import parse_datetime
import string
import random
import hashlib
from django.utils import timezone
from decimal import Decimal
from datetime import datetime,timedelta
import razorpay
from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
    return render(request, 'home/home.html')

@login_required
def transactions(request):
    user = request.user  # Get the current logged-in user
    transaction_type = request.GET.get('type')  # Get the transaction type from the query parameter
    start_date = request.GET.get('start_date')  # Get the start date from query parameters
    end_date = request.GET.get('end_date')  # Get the end date from query parameters
    
    # Base query for filtering transactions by user
    transactions = Transaction.objects.filter(user=user)
    
    # Filter by transaction type if provided
    if transaction_type in ['deposit', 'withdraw']:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    # Filter by date range if provided
    if start_date:
        try:
            start_date = parse_datetime(start_date)
            transactions = transactions.filter(created_at__gte=start_date)
        except ValueError:
            pass  # Ignore invalid date
    if end_date:
        try:
            end_date = parse_datetime(end_date)
            transactions = transactions.filter(created_at__lte=end_date)
        except ValueError:
            pass  # Ignore invalid date
    
    context = {
        'transactions': transactions,
    }
    return render(request, 'home/transaction.html', context)

@login_required
def my_account(request):
    wallet_balance = request.user.main_account_wallet + request.user.gaming_wallet
    context = {
        'wallet_balance':wallet_balance,
    }
    return render(request, 'home/account.html',context)

def transId(length=15):
    characters = string.ascii_letters + string.digits
    attempts = 0
    while True:
        transId = ''.join(random.choice(characters) for _ in range(length))
        if not Transaction.objects.filter(transaction_id=transId).exists():
            return transId
        attempts += 1


@login_required
def addFunds(request):
    if request.method == 'POST':
        gateway = GatewaySettings.objects.all().first()
        choice = gateway.payment_gateway
        amount = request.POST.get('amount')
        validator = PaymentSettings.objects.all().first()
        try:
            amount_decimal = Decimal(amount)
            if amount_decimal < validator.minimum_deposit:
                messages.error(request, f"Minimum deposit can't be below {validator.minimum_deposit}")
                return redirect('/my-account')
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount entered. Please enter a valid number.")
            return redirect('/my-account')
        if choice == 'razorpay':
            client = razorpay.Client(auth=(gateway.razorpay_api_key,gateway.razorpay_api_secret))
            payment = client.order.create({'amount':int(amount) * 100,'currency':'INR','payment_capture':1})
            request.user.order_id = payment['id']
            request.user.save()
            transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_id=payment['id']
            )

            context = {
                'payment':payment,
                'key':gateway.razorpay_api_key,
            }
            return render(request,'home/account.html',context)
        elif choice == 'payu':
            userid = request.user.phone_number
            MERCHANT_KEY = gateway.payu_merchant_key
            SALT = gateway.payu_merchant_salt
            txnid = transId()
            productInfo = "Spinzo Deposit"
            firstname = f'{request.user.phone_number}'
            email = 'spinzo@gmail.com'
            phone = request.user.phone_number
            hash_string = f"{MERCHANT_KEY}|{txnid}|{amount}|{productInfo}|{firstname}|{email}|{userid}||||||||||{SALT}"
            hash_value = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
            print('<h1 style="color:red;text-align:center;">Please Wait We are redirecting you on Payment Page</h1>')
            html_form = f"""
            <body>
            <form action="https://secure.payu.in/_payment" method="post" name="payuForm">
                  <input type="hidden" name="key" value="{MERCHANT_KEY}" />
                 <input type="hidden" name="hash" value="{hash_value}"/>
                 <input type="hidden" name="txnid" value="{txnid}" />
                <input type="hidden" name="amount" value="{amount}">
                <input type="hidden" name="productinfo" value="{productInfo}">
                <input type="hidden" name="firstname" value="{firstname}">
                <input type="hidden" name="email" value="{email}">
                <input type="hidden" name="phone" value="{phone}">
                <input type="hidden" name="mobile" value="{phone}">
                <input type="hidden" name="surl" value="http://127.0.0.1:8000/payment/success/">
                <input type="hidden" name="furl" value="http://127.0.0.1:8000/payment/failure/">
                <input type="hidden" name="udf1" value="{userid}">
                <input type="hidden" name="service_provider" value="payu_paisa" size="64" />
                <script>
                document.body.onload = function(ev){{
                     document.payuForm.submit();
                }}
                </script>
            </form>
            </body>
            """
            transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_id=txnid
            )

            return HttpResponse(html_form)
    return redirect('/transactions')

@login_required
@csrf_exempt
def razorpay_payment_status(request):
    if request.method == 'GET':
        try:
            # Extract payment details from the GET parameters
            razorpay_payment_id = request.GET.get('payment_id')
            razorpay_order_id = request.GET.get('order_id')
            razorpay_signature = request.GET.get('signature')
            gateway = GatewaySettings.objects.all().first()
            # Verify the payment signature
            params_dict = {
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': razorpay_signature
            }
            client = razorpay.Client(auth=(gateway.razorpay_api_key,gateway.razorpay_api_secret))
            client.utility.verify_payment_signature(params_dict)

            # Update the transaction in the database
            transaction = Transaction.objects.get(transaction_id=razorpay_order_id)
            transaction.status = 'success'
            transaction.save()
            request.user.main_account_wallet = request.user.main_account_wallet + Decimal(transaction.amount)
            request.user.save()

            messages.success(request,'Transaction Completed successfully.')
            return redirect('/transactions')
        
        except razorpay.errors.SignatureVerificationError:
            messages.error(request,'Invalid Transaction.')
            return redirect('/transactions')
        
        except Transaction.DoesNotExist:
            messages.error(request,'Invalid Transaction.')
            return redirect('/transactions')
        
        except Exception as e:
            messages.error(request,f'Invalid Transaction. {e}')
            return redirect('/transactions')

    return redirect('/transactions')