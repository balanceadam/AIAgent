from django.contrib import admin
from import_export.admin import ImportMixin

from account import models, resources
from generic.admin import BaseModelAdmin


@admin.register(models.Account)
class AccountAdmin(BaseModelAdmin):
    list_display = ['id', 'name', 'invite_code', 'avatar', 'address', 'created_at', 'updated_at', 'is_enabled']
    list_filter = ['is_enabled', 'created_at']
    search_fields = ['name', 'invite_code', 'walletaddress_set__address']


@admin.register(models.WhitelistAddress)
class WhitelistAddressAdmin(ImportMixin, BaseModelAdmin):
    resource_class = resources.WhitelistAddressResource
    list_display = ['id', 'address', 'batch', 'created_at', 'is_enabled']
    search_fields = ['address', 'batch']
    fields = ['address', 'batch']
    list_filter = ['batch', 'created_at']


@admin.register(models.NameChangeLog)
class NameChangeLogAdmin(ImportMixin, BaseModelAdmin):
    list_display = ['id', 'account', 'name', 'created_at', 'is_enabled']
    autocomplete_fields = ['account']
