# Generated by Django 4.0 on 2024-10-21 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_alter_assetstoken_options_remove_protocol_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='protocol',
            name='bonding_curve',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='protocol',
            name='day_increase',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='protocol',
            name='day_trading_volume',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='protocol',
            name='market_value',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
    ]
