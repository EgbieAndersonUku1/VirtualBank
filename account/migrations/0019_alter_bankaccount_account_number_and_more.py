# Generated by Django 5.2.3 on 2025-07-09 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_alter_bankaccount_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='account_number',
            field=models.CharField(db_index=True, default='55284769', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='sort_code',
            field=models.CharField(db_index=True, default='760345', max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='wallet_id',
            field=models.CharField(default='50880147577', unique=True),
        ),
    ]
