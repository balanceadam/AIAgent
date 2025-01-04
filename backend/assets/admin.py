from django.contrib import admin

from assets import models
from generic.admin import BaseModelAdmin


@admin.register(models.AssetsChain)
class AssetsChainAdmin(BaseModelAdmin):
    list_display = ['id', 'name', 'logo', 'fee', 'symbol', 'sort', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(models.FillingService)
class FillingServiceAdmin(BaseModelAdmin):
    list_display = ['id', 'name', 'logo', 'description', 'sort', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(models.AssetsGame)
class AssetsGameAdmin(BaseModelAdmin):
    list_display = ['id', 'name', 'img', 'logo', 'sort', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(models.AssetsToken)
class AssetsTokenAdmin(BaseModelAdmin):
    list_display = [
        'id', 'account', 'protocol', 'name', 'epal_name', 'ticker', 'telegram', 'website', 'twitter', 'logo', 'epal',
        'description', 'chain', 'initial_buy_type', 'initial_buy_number', 'labels', 'sort', 'created_at', 'updated_at'
    ]
    search_fields = ['name', 'account__name', 'protocol__address']
    autocomplete_fields = ['account', 'chain', 'filling_services', 'games', 'protocol']


@admin.register(models.Protocol)
class ProtocolAdmin(BaseModelAdmin):
    list_display = [
        'id', 'protocol_id', 'address', 'symbol', 'price', 'bonding_curve', 'market_value', 'day_increase',
        'day_trading_volume', 'created_at', 'updated_at'
    ]
    search_fields = ['address', 'protocol_id', 'symbol']


@admin.register(models.MinuteMarketData)
class MinuteMarketDataAdmin(BaseModelAdmin):
    list_display = ['id', 'protocol', 'open', 'close', 'high', 'low', 'volume', 'time', 'created_at']
    search_fields = ['protocol__id', 'protocol__protocol_id']
    autocomplete_fields = ['protocol']


@admin.register(models.DayMarketData)
class DayMarketDataAdmin(BaseModelAdmin):
    list_display = ['id', 'protocol', 'open', 'close', 'high', 'low', 'volume', 'market_value', 'date', 'created_at']
    search_fields = ['protocol__id', 'protocol__protocol_id']
    autocomplete_fields = ['protocol']


@admin.register(models.Position)
class PositionAdmin(BaseModelAdmin):
    list_display = ['id', 'account', 'token', 'position', 'updated_at']
    search_fields = ['account__name', 'token__protocol__address']
    autocomplete_fields = ['account', 'token']


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'token', 'type', 'quantity', 'amount', 'time', 'hash', 'created_at']
    search_fields = ['account__name', 'token__protocol__address']
    autocomplete_fields = ['account', 'token']
