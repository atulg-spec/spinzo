from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.
@admin.register(SiteSettings)
class SiteIconAdmin(admin.ModelAdmin):
    list_display = ('icon_preview','siteName')

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 80px; height: 50px; border-radius: 5px;" alt="{}">',
                obj.icon.url,
                'icon',
            )
        return "No Icon"
    icon_preview.short_description = "Logo Image"

@admin.register(GatewaySettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('mode', 'payment_gateway', 'get_gateway_keys', 'get_gateway_secrets')
    list_filter = ('mode', 'payment_gateway')  # Filters for easy navigation
    search_fields = ('razorpay_api_key', 'payu_merchant_key')  # Searchable fields

    # Organize fields in the detail view
    fieldsets = (
        ('General Settings', {
            'fields': ('mode', 'payment_gateway'),
            'description': 'Select the operating mode and payment gateway.',
        }),
        ('Razorpay Settings', {
            'fields': ('razorpay_api_key', 'razorpay_api_secret'),
            'classes': ('collapse',),  # Collapsible section for cleaner UI
        }),
        ('PayU Settings', {
            'fields': ('payu_merchant_key', 'payu_merchant_salt'),
            'classes': ('collapse',),  # Collapsible section for cleaner UI
        }),
    )
    
    # Read-only helper methods to display concatenated keys and secrets
    @admin.display(description="Gateway Keys")
    def get_gateway_keys(self, obj):
        if obj.payment_gateway == 'razorpay':
            return obj.razorpay_api_key or "Not Set"
        elif obj.payment_gateway == 'payu':
            return obj.payu_merchant_key or "Not Set"
        return "N/A"

    @admin.display(description="Gateway Secrets")
    def get_gateway_secrets(self, obj):
        if obj.payment_gateway == 'razorpay':
            return '********' or "Not Set"
        elif obj.payment_gateway == 'payu':
            return '********' or "Not Set"
        return "N/A"

@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'minimum_withdrawal', 'minimum_deposit')
    # list_editable = ('minimum_withdrawal', 'minimum_deposit')
    search_fields = ('id',)
    ordering = ('id',)
    list_per_page = 25

    # Optional: Add tooltips or additional help in the admin interface
    fieldsets = (
        (None, {
            'fields': ('minimum_withdrawal', 'minimum_deposit'),
            'description': 'Manage the payment settings for withdrawals and deposits.'
        }),
    )

@admin.register(RewardSettings)
class RewardSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'signup_reward', 
        'first_deposit_reward', 
        'second_deposit_reward', 
        'third_deposit_reward',
        'referral_commission_level_1',
        'referral_commission_level_2',
        'referral_commission_level_3',
        'referral_commission_level_4',
        'referral_commission_level_5',
        'referral_commission_level_6',
        'referral_commission_level_7'
    )
    search_fields = ('id',)  # Optionally, you can search by ID
    list_filter = ('first_deposit_reward', 'second_deposit_reward', 'third_deposit_reward')  # Filter by deposit reward percentages
    ordering = ('id',)  # Default ordering by ID

    # Optional: You can add additional customization like fieldsets or inlines if needed
    fieldsets = (
        ('Sign Up', {
            'fields': (
                'signup_reward',
            )
        }),
        ('Deposit Reward', {
            'fields': (
                'first_deposit_reward',
                'second_deposit_reward',
                'third_deposit_reward',
            )
        }),
        ('Referral', {
            'fields': (
                'referral_commission_level_1',
                'referral_commission_level_2',
                'referral_commission_level_3',
                'referral_commission_level_4',
                'referral_commission_level_5',
                'referral_commission_level_6',
                'referral_commission_level_7',
            )
        }),

    )

