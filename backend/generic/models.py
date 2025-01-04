import binascii
import json
import os
import random, uuid
import string

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from generic import constants, queryset


class BaseModel(models.Model):
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RequestLog(BaseModel):
    trade_id = models.CharField(max_length=128)
    service = models.CharField(max_length=128)
    url = models.CharField(max_length=200)
    request_at = models.DateTimeField()
    response_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _("Request Log")
        verbose_name_plural = _("Request Log")
        db_table = "generic_request_log"

    def __str__(self):
        return self.trade_id


class RequestLogDetail(BaseModel):
    log = models.OneToOneField(RequestLog, on_delete=models.CASCADE)
    request = models.TextField()
    response = models.TextField()

    class Meta:
        verbose_name = _("Request Log Detail")
        verbose_name_plural = _("Request Log Detail")
        db_table = "generic_request_log_detail"

    def __str__(self):
        return f'{self.log_id}'


class BasicInfo(BaseModel):
    type = models.PositiveSmallIntegerField(choices=constants.BasicInfoType.CHOICES)
    name = models.CharField(max_length=100)
    value = models.TextField(null=True, blank=True)
    objects = queryset.BasicInfoQuerySet.as_manager()

    class Meta:
        verbose_name = _("Basic Info")
        verbose_name_plural = _("Basic Info")
        db_table = "generic_basic_info"
        ordering = ('type', '-created_at',)

    def __str__(self):
        return f'{self.get_type_display()}-{self.name}'
