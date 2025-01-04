import base64
import datetime
from decimal import Decimal
import json
import random
import re
import string

from bs4 import BeautifulSoup
from django.conf import settings
from django.db.models import Sum


def generate_random_str(length: int = 15, include_punctuation: bool = True) -> str:
    letters = string.digits + string.ascii_letters
    if include_punctuation:
        letters += string.punctuation
    return ''.join(random.sample(letters, length))


def getattr_sum_or_zero(qs, name):
    """
    获取queryset某个字段求和的值,如果qs为空,返回0
    :param qs:
    :param name:
    :return:
    """
    return qs.aggregate(Sum(name))[name+"__sum"] or 0 if qs.exists() else 0


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return round(float(obj), 2)
        return json.JSONEncoder.default(self, obj)


def judge_version(version1, version2):
    """
    判断version1是否大于version2,是则返回True,否则返回False
    :param version1:
    :param version2:
    :return:
    """
    try:
        d1 = re.split('\.', version1)
        d2 = re.split('\.', version2)

        v1 = [int(d1[i]) for i in range(len(d1))]
        v2 = [int(d2[i]) for i in range(len(d2))]

        return v1 > v2
    except (Exception,):
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # In case there are multiple addresses, take the first one.
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def is_phone_valid(phone):
    """
    校验中国手机号是否有效
    :param phone: str, 要校验的手机号
    :return: bool, 如果手机号有效返回 True，否则返回 False
    """
    # 定义中国手机号的正则表达式模式
    pattern = re.compile(r"^1[3-9]\d{9}$")

    # 使用正则表达式进行匹配
    return bool(pattern.match(phone))


def get_server_ip():
    return settings.SERVER_IP


def get_server_https_host(request):
    return 'https://' + request.get_host()


def img_to_base64(img):
    content = img.read()
    img_base64 = base64.b64encode(content).decode('utf-8')
    return img_base64


def get_time_str(format_str='%Y%m%d%H%M%S'):
    return datetime.datetime.now().strftime(format_str)


def is_azure_storage():
    return settings.DEFAULT_FILE_STORAGE in (
        'generic.custom_storages.AzureSASStorage', 'generic.custom_storages.AzureCDNStorage'
    )
