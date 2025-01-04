import json

from django.conf import settings
from django.core.cache import cache
from django.db import models

from generic import constants


class BasicInfoQuerySet(models.query.QuerySet):
    pass
