# Generated by Django 4.0 on 2024-10-07 14:41

import assets.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetsChain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('logo', models.ImageField(upload_to=assets.models.upload_chain_logo)),
                ('fee', models.DecimalField(decimal_places=2, max_digits=6)),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('sort', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Assets Chain',
                'verbose_name_plural': 'Assets Chains',
                'db_table': 'assets_chain',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='FillingService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to=assets.models.upload_service_logo)),
                ('sort', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Filling Service',
                'verbose_name_plural': 'Filling Service',
                'db_table': 'assets_filling_service',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='AssetsToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('telegram', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('logo', models.ImageField(upload_to=assets.models.upload_token_logo)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.assetschain')),
                ('filling_services', models.ManyToManyField(to='assets.FillingService')),
            ],
            options={
                'verbose_name': 'Assets Token',
                'verbose_name_plural': 'Assets Tokens',
                'db_table': 'assets_token',
                'ordering': ('-created_at',),
            },
        ),
    ]
