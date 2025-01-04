import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from generic.models import BaseModel
from generic.utils import get_time_str, is_azure_storage


def upload_avatar(instance, filename):
    return f'account/avatar/{instance.name}/{get_time_str()}/{filename}'


class Account(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, db_index=True)
    invite_code = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to=upload_avatar, null=True, blank=True)
    token_count = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Account'
        db_table = "account_account"
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    @property
    def address(self):
        account_address = self.walletaddress_set.first()
        return account_address.address if account_address else ''


class WhitelistAddress(BaseModel):
    address = models.CharField(max_length=255, db_index=True)
    batch = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Whitelist Address'
        verbose_name_plural = 'Whitelist Address'
        db_table = "account_whitelist_address"
        ordering = ('-created_at',)


class NameChangeLog(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Name Change Log'
        verbose_name_plural = 'Name Change Log'
        db_table = "account_name_change_log"
        ordering = ('-created_at',)
