# Generated by Django 5.2.3 on 2025-07-04 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0022_alter_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='code',
            field=models.CharField(db_index=True, default='900989226', max_length=9),
        ),
    ]
