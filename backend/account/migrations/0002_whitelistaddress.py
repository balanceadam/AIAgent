# Generated by Django 4.0 on 2024-10-18 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhitelistAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(db_index=True, max_length=255)),
                ('batch', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Whitelist Address',
                'verbose_name_plural': 'Whitelist Address',
                'db_table': 'account_whitelist_address',
                'ordering': ('-created_at',),
            },
        ),
    ]
