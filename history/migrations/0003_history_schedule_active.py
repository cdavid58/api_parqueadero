# Generated by Django 3.2.8 on 2023-07-17 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_auto_20230708_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='history_schedule',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
