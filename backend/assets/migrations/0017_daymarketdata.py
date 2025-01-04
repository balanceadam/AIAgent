# Generated by Django 4.0 on 2024-12-22 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0016_assetsgame_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayMarketData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('open', models.DecimalField(decimal_places=20, default=0, max_digits=60)),
                ('close', models.DecimalField(decimal_places=20, default=0, max_digits=60)),
                ('high', models.DecimalField(decimal_places=20, default=0, max_digits=60)),
                ('low', models.DecimalField(decimal_places=20, default=0, max_digits=60)),
                ('volume', models.DecimalField(decimal_places=20, default=0, max_digits=60)),
                ('market_value', models.DecimalField(decimal_places=20, default=0, max_digits=60)),
                ('date', models.DateField(db_index=True)),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.protocol')),
            ],
            options={
                'verbose_name': 'Day Market Data',
                'verbose_name_plural': 'Day Market Data',
                'db_table': 'assets_day_market_data',
                'ordering': ('-created_at',),
                'unique_together': {('protocol', 'date')},
            },
        ),
    ]
