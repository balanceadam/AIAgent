from django.db import models

from generic.models import BaseModel


class Network(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    rpc_url = models.CharField(max_length=255, null=True, blank=True)
    chain_id = models.CharField(max_length=20, unique=True)
    currency = models.CharField(max_length=20, null=True, blank=True)
    block_explorer_url = models.CharField(max_length=255, null=True, blank=True)
    api_url = models.CharField(max_length=255, null=True, blank=True)
    api_token = models.CharField(max_length=255, null=True, blank=True)
    last_page = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Network'
        db_table = "wallet_network"
        ordering = ('-created_at',)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Chain Id %s" % self.chain_id


class WalletAddress(BaseModel):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, db_index=True)

    class Meta:
        verbose_name = 'Wallet Address'
        verbose_name_plural = 'Wallet Address'
        db_table = "wallet_wallet_address"
        ordering = ('-created_at',)
        unique_together = (('network', 'address'),)

    @property
    def encrypted_address(self):
        if not self.address:
            return ''
        if len(self.address) > 10:
            return self.address[:6] + '***' + self.address[-4::]
        return self.address[:1] + '***' + self.address[-1:]
