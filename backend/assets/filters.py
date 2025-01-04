import django_filters as filters
from django.db.models import Q

from assets import models


class AssetsTokenFilter(filters.FilterSet):
    bondingCurve = filters.NumberFilter(field_name='protocol__bonding_curve', lookup_expr='exact')
    chain = filters.NumberFilter(field_name='chain_id', lookup_expr='exact')
    accountId = filters.NumberFilter(field_name='account_id')
    ordering = filters.OrderingFilter(
        fields=(
            ('created_at', 'createdAt'),
            ('protocol__market_value', 'marketValue'),
            ('protocol__day_increase', 'dayIncrease'),
            ('protocol__day_trading_volume', 'dayTradingVolume'),
        )
    )

    class Meta:
        model = models.AssetsToken
        fields = ['bondingCurve', 'chain', 'accountId']


class TransactionsFilter(filters.FilterSet):
    tokenId = filters.NumberFilter(field_name='token_id', lookup_expr='exact')

    class Meta:
        model = models.Transaction
        fields = ['tokenId']