# Generated by Django 5.1.4 on 2024-12-14 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('following', '0003_alter_follow_created'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]