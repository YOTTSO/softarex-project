# Generated by Django 5.1a1 on 2024-06-19 18:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0002_useracc_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='UserAcc',
        ),
    ]