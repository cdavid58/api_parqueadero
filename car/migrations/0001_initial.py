# Generated by Django 3.2.8 on 2023-07-08 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.CharField(max_length=10, unique=True)),
                ('type_car', models.CharField(max_length=7)),
            ],
        ),
    ]
