# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TeamMembership

class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    fk_name = 'user'  # Specify the ForeignKey field in TeamMembership that relates to CustomUser
    extra = 1  # Number of empty forms displayed for adding new relationships

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone_number', 'gaming_wallet', 'main_account_wallet', 'city', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('region_name', 'city', 'zip_code', 'lat', 'lon', 'timezone', 'isp')}),
        ('Wallets', {'fields': ('gaming_wallet', 'main_account_wallet')}),
        ('Referrals', {'fields': ('referral_code', 'user_invited_by')}),  # Removed 'team_members'
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_active')},
        ),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    inlines = [TeamMembershipInline]  # Add the inline for managing team members

admin.site.register(CustomUser, CustomUserAdmin)
