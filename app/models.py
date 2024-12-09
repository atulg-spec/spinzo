from django.db import models

class SiteSettings(models.Model):
    siteName = models.CharField(default="Spinzo",max_length=20)
    icon = models.ImageField(upload_to='site_icons/', verbose_name="Site Icon")

    def __str__(self):
        return f"Icon {self.id}"
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

class GatewaySettings(models.Model):
    MODE_CHOICES = [
        ('test', 'Test Mode'),
        ('live', 'Live Mode'),
    ]
    
    GATEWAY_CHOICES = [
        ('payu', 'PayU'),
        ('razorpay', 'Razorpay'),
    ]
    
    mode = models.CharField(
        max_length=10,
        choices=MODE_CHOICES,
        default='test',
        help_text="Select the operating mode for the payment gateway."
    )
    payment_gateway = models.CharField(
        max_length=10,
        choices=GATEWAY_CHOICES,
        default='razorpay',
        help_text="Select the payment gateway to be used."
    )
    razorpay_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter Razorpay API Key."
    )
    razorpay_api_secret = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter Razorpay API Secret."
    )
    payu_merchant_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter PayU Merchant Key."
    )
    payu_merchant_salt = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter PayU Merchant Salt."
    )
    
    def __str__(self):
        return f"{self.mode} - {self.payment_gateway}"
    
    class Meta:
        verbose_name = "Gateway Setting"
        verbose_name_plural = "Gateway Settings"

class PaymentSettings(models.Model):
    minimum_withdrawal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        help_text="Minimum amount allowed for withdrawal"
    )
    minimum_deposit = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        help_text="Minimum amount allowed for deposit"
    )

    def __str__(self):
        return f"Payment Settings (ID: {self.id})"

    class Meta:
        verbose_name = "Payment Setting"
        verbose_name_plural = "Payment Settings"


class RewardSettings(models.Model):
    signup_reward = models.FloatField(
        verbose_name="Signup Reward", 
        help_text="Reward given upon user signup",
        default=0.0  # Set a default value (e.g., 0.0 for no reward)
    )
    first_deposit_reward = models.FloatField(
        verbose_name="First Deposit Reward Percentage", 
        help_text="Percentage reward for the first deposit",
        default=10.0  # Default 10% reward
    )
    second_deposit_reward = models.FloatField(
        verbose_name="Second Deposit Reward Percentage", 
        help_text="Percentage reward for the second deposit",
        default=7.5  # Default 7.5% reward
    )
    third_deposit_reward = models.FloatField(
        verbose_name="Third Deposit Reward Percentage", 
        help_text="Percentage reward for the third deposit",
        default=5.0  # Default 5% reward
    )
    
    referral_commission_level_1 = models.FloatField(
        verbose_name="Referral Commission Level 1", 
        help_text="Referral commission percentage for Level 1",
        default=10.0  # Default 10% commission for level 1
    )
    referral_commission_level_2 = models.FloatField(
        verbose_name="Referral Commission Level 2", 
        help_text="Referral commission percentage for Level 2",
        default=7.0  # Default 7% commission for level 2
    )
    referral_commission_level_3 = models.FloatField(
        verbose_name="Referral Commission Level 3", 
        help_text="Referral commission percentage for Level 3",
        default=5.0  # Default 5% commission for level 3
    )
    referral_commission_level_4 = models.FloatField(
        verbose_name="Referral Commission Level 4", 
        help_text="Referral commission percentage for Level 4",
        default=3.0  # Default 3% commission for level 4
    )
    referral_commission_level_5 = models.FloatField(
        verbose_name="Referral Commission Level 5", 
        help_text="Referral commission percentage for Level 5",
        default=2.5  # Default 2.5% commission for level 5
    )
    referral_commission_level_6 = models.FloatField(
        verbose_name="Referral Commission Level 6", 
        help_text="Referral commission percentage for Level 6",
        default=2.0  # Default 2% commission for level 6
    )
    referral_commission_level_7 = models.FloatField(
        verbose_name="Referral Commission Level 7", 
        help_text="Referral commission percentage for Level 7",
        default=1.5  # Default 1.5% commission for level 7
    )
    
    def __str__(self):
        return f"Reward Settings (ID: {self.id})"
    
    class Meta:
        verbose_name = "Reward Setting"
        verbose_name_plural = "Reward Settings"
