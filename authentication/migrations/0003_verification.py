# Generated by Django 5.2.3 on 2025-06-15 19:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, default='182161423', max_length=9)),
                ('num_of_days_to_expire', models.PositiveSmallIntegerField(default=1)),
                ('description', models.CharField(max_length=255)),
                ('verify_by', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'code'], name='authenticat_user_id_db3f4a_idx')],
            },
        ),
    ]
