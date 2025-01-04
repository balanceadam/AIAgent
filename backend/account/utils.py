import uuid

from django.conf import settings
from rest_framework.authtoken.models import Token

from account import models
from generic.exceptions import ValidateError
from generic.utils import generate_random_str


def get_and_refresh_token(address):
    account = models.Account.objects.get(walletaddress__address=address)
    if not account:
        raise ValidateError('Address is invalid')
    if Token.objects.filter(user=account.user).exists():
        Token.objects.filter(user=account.user).delete()  # 刷新token
    token, created = Token.objects.get_or_create(user=account.user)
    return token.key


def get_token(address):
    account = models.Account.objects.get(walletaddress__address=address)
    if not account:
        raise ValidateError('Address is invalid')
    token, created = Token.objects.get_or_create(user=account.user)
    return token.key


def get_token_by_user(user):
    token, created = Token.objects.get_or_create(user=user)
    return token.key


def generate_uid():
    return uuid.uuid4().hex[:16]


def create_account(address):
    username = generate_uid()
    while models.User.objects.filter(username=username).exists():
        username = generate_uid()
    user = models.User.objects.create_user(username, password=generate_random_str(20))
    invite_code = generate_random_str(8, False)
    while models.Account.objects.filter(invite_code=invite_code).exists():
        invite_code = generate_random_str(8, False)
    account = models.Account.objects.create(
        user=user, name='@' + address[:6], invite_code=invite_code
    )
    return account
