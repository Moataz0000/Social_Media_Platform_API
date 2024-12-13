# Generated by Django 5.1.4 on 2024-12-13 11:15

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_user_id_alter_user_name_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7e3ac830-7494-4944-9a0e-27b45c60ea83'), editable=False, primary_key=True, serialize=False),
        ),
    ]