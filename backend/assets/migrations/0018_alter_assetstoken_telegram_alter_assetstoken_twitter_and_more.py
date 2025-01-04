# Generated by Django 4.0 on 2024-12-24 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0017_daymarketdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetstoken',
            name='telegram',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='assetstoken',
            name='twitter',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='assetstoken',
            name='website',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
