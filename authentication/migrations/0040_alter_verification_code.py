# Generated by Django 5.2.3 on 2025-07-18 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0039_alter_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='code',
            field=models.CharField(db_index=True, default='423228038', max_length=9),
        ),
    ]
