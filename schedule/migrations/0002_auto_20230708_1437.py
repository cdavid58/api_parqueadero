# Generated by Django 3.2.8 on 2023-07-08 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot', '0001_initial'),
        ('user', '0002_user_type_user'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='parking_lot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parking_lot.parking_lot'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]