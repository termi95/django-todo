# Generated by Django 5.1.3 on 2024-12-05 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0002_remove_todoitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todoitem',
            name='category',
        ),
    ]