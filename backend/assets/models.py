from django.db import models

from assets import constants
from generic.models import BaseModel
from generic.utils import get_time_str


def upload_chain_logo(instance, filename):
    return f'assets/chain/{instance.name}/{get_time_str()}/{filename}'


class AssetsChain(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to=upload_chain_logo)
    fee = models.DecimalField(max_digits=6, decimal_places=2)
    symbol = models.CharField(max_length=10, unique=True)
    sort = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Assets Chain'
        verbose_name_plural = 'Assets Chains'
        db_table = "assets_chain"
        ordering = ('sort',)

    def __str__(self):
        return self.name


def upload_service_logo(instance, filename):
    return f'assets/service/{instance.name}/{get_time_str()}/{filename}'


class FillingService(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)
    logo = models.ImageField(upload_to=upload_service_logo)
    sort = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Filling Service'
        verbose_name_plural = 'Filling Service'
        db_table = "assets_filling_service"
        ordering = ('sort',)

    def __str__(self):
        return self.name


def upload_game_img(instance, filename):
    return f'assets/game/{instance.name}/{get_time_str()}/{filename}'


def upload_game_logo(instance, filename):
    return f'assets/game/logo/{instance.name}/{get_time_str()}/{filename}'


class AssetsGame(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    img = models.ImageField(upload_to=upload_game_img)
    logo = models.ImageField(upload_to=upload_game_logo, null=True, blank=True)
    sort = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Assets Game'
        verbose_name_plural = 'Assets Game'
        db_table = "assets_game"
        ordering = ('sort',)


def upload_token_logo(instance, filename):
    return f'assets/token/logo/{instance.ticker}/{get_time_str()}/{filename}'


def upload_token_epal(instance, filename):
    return f'assets/token/epal/{instance.ticker}/{get_time_str()}/{filename}'


class Protocol(BaseModel):
    protocol_id = models.PositiveBigIntegerField(db_index=True)
    address = models.CharField(max_length=255, db_index=True)
    symbol = models.CharField(max_length=50, db_index=True, default='')
    price = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    bonding_curve = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    market_value = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    volume = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    day_increase = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    day_trading_volume = models.DecimalField(max_digits=60, decimal_places=20, default=0)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Protocol'
        verbose_name_plural = 'Protocol'
        db_table = "assets_protocol"
        ordering = ('-created_at',)


class AssetsToken(BaseModel):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    epal_name = models.CharField(max_length=20, unique=True, default='')
    ticker = models.CharField(max_length=10, unique=True)
    telegram = models.CharField(max_length=25, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.URLField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    logo = models.ImageField(upload_to=upload_token_logo)
    epal = models.ImageField(upload_to=upload_token_epal, null=True, blank=True)
    chain = models.ForeignKey(AssetsChain, on_delete=models.CASCADE)
    filling_services = models.ManyToManyField(FillingService)
    initial_buy_type = models.PositiveSmallIntegerField(choices=constants.AssetsTokenInitialBuyType.CHOICES, default=1)
    initial_buy_number = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    games = models.ManyToManyField(AssetsGame)
    labels = models.CharField(max_length=500, null=True, blank=True)
    sort = models.PositiveSmallIntegerField(default=100)
    protocol = models.OneToOneField(Protocol, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Assets Token'
        verbose_name_plural = 'Assets Tokens'
        db_table = "assets_token"
        ordering = ('sort', '-created_at',)

    def __str__(self):
        return self.name


class MinuteMarketData(BaseModel):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    open = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    close = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    high = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    low = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    volume = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    time = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.protocol.address

    class Meta:
        verbose_name = 'Minute Market Data'
        verbose_name_plural = 'Minute Market Data'
        db_table = "assets_minute_market_data"
        ordering = ('-created_at',)
        unique_together = ('protocol', 'time')


class DayMarketData(BaseModel):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    open = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    close = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    high = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    low = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    volume = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    market_value = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    date = models.DateField(db_index=True)

    def __str__(self):
        return self.protocol.address

    class Meta:
        verbose_name = 'Day Market Data'
        verbose_name_plural = 'Day Market Data'
        db_table = "assets_day_market_data"
        ordering = ('-created_at',)
        unique_together = ('protocol', 'date')


class Position(BaseModel):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    token = models.ForeignKey(AssetsToken, on_delete=models.CASCADE)
    position = models.DecimalField(max_digits=60, decimal_places=20, default=0)

    def __str__(self):
        return self.account.name + self.token.name

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Position'
        db_table = "assets_position"
        ordering = ('-created_at',)


class Transaction(BaseModel):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    token = models.ForeignKey(AssetsToken, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    amount = models.DecimalField(max_digits=60, decimal_places=20, default=0)
    time = models.DateTimeField()
    hash = models.CharField(max_length=255)

    def __str__(self):
        return self.account.name + self.token.name

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transaction'
        db_table = "assets_transaction"
        ordering = ('-time',)

    @property
    def format_hash(self):
        return self.hash[:6] + '...' + self.hash[-4:]
