from collections import OrderedDict
import logging

from django.shortcuts import render
from djangorestframework_camel_case.util import underscoreize
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from generic import permissions, models, serializers, filters, utils, constants
from generic.exceptions import ValidateError

logger = logging.getLogger('main')


class BaseAPIMixin:
    data = None
    serializer = None
    serializer_class = None
    authentication_classes = permissions.authentication_classes['basic']

    def get_data(self, request):
        self.serializer = self.serializer_class(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.data = self.serializer.validated_data
        return self.data

    def get_query_params(self, request):
        self.serializer = self.serializer_class(data=underscoreize(request.query_params))
        self.serializer.is_valid(raise_exception=True)
        self.data = self.serializer.validated_data
        return self.data


class LoginMixin(BaseAPIMixin):
    authentication_classes = permissions.authentication_classes['basic']
    permission_classes = permissions.permission_classes['login']


class BasicInfoListView(generics.ListAPIView):
    """
    基础信息列表
    """
    queryset = models.BasicInfo.objects.filter(is_enabled=True)
    serializer_class = serializers.BasicInfoModelSerializer
    filterset_class = filters.BasicInfoFilter
    pagination_class = None
