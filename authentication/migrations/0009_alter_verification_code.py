# Generated by Django 5.2.3 on 2025-06-27 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_user_surname_alter_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='code',
            field=models.CharField(db_index=True, default='927569860', max_length=9),
        ),
    ]
