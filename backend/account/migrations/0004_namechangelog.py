# Generated by Django 4.0 on 2024-12-24 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_account_token_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='NameChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, max_length=10)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
            options={
                'verbose_name': 'Name Change Log',
                'verbose_name_plural': 'Name Change Log',
                'db_table': 'account_name_change_log',
                'ordering': ('-created_at',),
            },
        ),
    ]
