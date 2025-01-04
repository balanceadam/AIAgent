import django_filters as filters
from django.db.models import Q

from social import models


class CommentFilter(filters.FilterSet):
    tokenId = filters.NumberFilter(field_name='token_id', lookup_expr='exact')

    class Meta:
        model = models.Comment
        fields = ['tokenId',]


class FansFilter(filters.FilterSet):
    accountId = filters.CharFilter(field_name='account_id')

    class Meta:
        model = models.Fans
        fields = ['accountId']


class FollowingsFilter(filters.FilterSet):
    accountId = filters.CharFilter(field_name='follower_id')

    class Meta:
        model = models.Fans
        fields = ['accountId']
