# Generated by Django 5.2.3 on 2025-07-04 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='code',
            field=models.CharField(db_index=True, default='218784084', max_length=9),
        ),
    ]
