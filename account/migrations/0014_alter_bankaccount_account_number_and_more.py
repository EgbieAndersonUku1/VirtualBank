# Generated by Django 5.2.3 on 2025-07-04 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_bankaccount_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='account_number',
            field=models.CharField(db_index=True, default='90291084', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='sort_code',
            field=models.CharField(db_index=True, default='453024', max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='wallet_id',
            field=models.CharField(default='18425903773', unique=True),
        ),
    ]
