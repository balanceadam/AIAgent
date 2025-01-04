from django.contrib import admin

from generic.admin import BaseModelAdmin
from wallet import models


@admin.register(models.Network)
class NetworkAdmin(BaseModelAdmin):
    list_display = [
        'id', 'name', 'rpc_url', 'chain_id', 'currency', 'block_explorer_url', 'api_url', 'api_token', 'last_page',
        'created_at'
    ]
    search_fields = ['name']


@admin.register(models.WalletAddress)
class WalletAddressAdmin(BaseModelAdmin):
    list_display = ['id', 'account', 'network', 'address', 'created_at']
    search_fields = ['address', 'account__name']
    list_filter = ['network']
    autocomplete_fields = ['account', 'network']
