# Generated by Django 5.1.4 on 2024-12-11 01:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('cc109272-6ece-4646-9201-3e0bc03b714f'), editable=False, primary_key=True, serialize=False),
        ),
    ]