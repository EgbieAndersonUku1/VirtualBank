# Generated by Django 5.2.3 on 2025-07-03 18:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='signature',
            field=models.ForeignKey(choices=[('u', 'Upload signature'), ('d', 'Draw signature')], null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='identification_signature', to='account.identificationdocument'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='account_number',
            field=models.CharField(db_index=True, default='06620902', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='sort_code',
            field=models.CharField(db_index=True, default='425929', max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='identification_documents',
            field=models.ForeignKey(choices=[('p', 'Passport'), ('d', 'Driving Licence'), ('n', 'National ID')], null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='identification_documents', to='account.identificationdocument'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='wallet_id',
            field=models.CharField(default='19778127411', unique=True),
        ),
    ]
