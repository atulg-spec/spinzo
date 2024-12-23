from django.contrib import admin
from .models import *

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'amount', 'status', 'transaction_type','created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_id', 'user__phone_number')
    ordering = ('-created_at',)
    # readonly_fields = ('transaction_id', 'created_at', 'updated_at')
