from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from assets import models
from generic.utils import getattr_sum_or_zero


class Command(BaseCommand):
    def handle(self, *args, **options):
        date = now().replace(hour=0, minute=0, second=0, microsecond=0)
        last_date = date - timedelta(days=1)
        for p in models.Protocol.objects.filter(is_enabled=True):
            day_data = models.MinuteMarketData.objects.filter(protocol=p, time__lte=date, time__gt=last_date)
            d, _ = models.DayMarketData.objects.get_or_create(
                protocol=p, date=date.date(), defaults={
                    'open': p.price, 'close': p.price, 'high': p.price, 'low': p.price, 'volume': 0,
                    'market_value': p.market_value,
                }
            )
            if day_data:
                d.open = day_data.order_by('time').first().open
                d.close = day_data.order_by('-time').first().close
                d.high = day_data.order_by('-high').first().high
                d.low = day_data.order_by('low').first().low
                d.volume = getattr_sum_or_zero(day_data, 'volume')
                d.market_value = p.market_value
                d.save()
            p.day_trading_volume = d.volume
            last_d = models.DayMarketData.objects.filter(protocol=p, date=last_date.date()).first()
            if last_d and last_d.market_value:
                p.day_increase = 100 * (d.market_value - last_d.market_value) / last_d.market_value
            else:
                p.day_increase = 0
            p.save()
