# Generated by Django 3.2.8 on 2023-07-22 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_fee_type_car'),
    ]

    operations = [
        migrations.CreateModel(
            name='Range_Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Fee',
        ),
    ]