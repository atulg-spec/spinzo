# Generated by Django 4.2.7 on 2024-12-23 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')], default='deposit', max_length=10),
        ),
    ]
