# Generated by Django 5.1.4 on 2024-12-16 01:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1ebdabd5-b501-4d08-9276-269c655aed14'), editable=False, primary_key=True, serialize=False),
        ),
    ]
