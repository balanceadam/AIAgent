from django.shortcuts import render
from django.utils.timezone import now
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.views import APIView, Response

from account import models, serializers
from assets.models import AssetsToken
from generic.exceptions import ValidateError
from generic.views import BaseAPIMixin, LoginMixin


class AccountInfoView(LoginMixin, APIView):
    serializer_class = serializers.AccountInfoSerializer

    @swagger_auto_schema(operation_description='用户信息', responses={200: serializer_class()})
    def get(self, request, *args, **kwargs):
        account = request.user.account
        data = self.serializer_class(account, context={'request': request}).data
        data['show_launch_button'] = models.WhitelistAddress.objects.filter(address=request.user.account.address).exists() and AssetsToken.objects.filter(account=account, protocol__isnull=False).count() < account.token_count
        return Response(data)

    @swagger_auto_schema(operation_description='修改用户信息', request_body=serializers.AccountInfoReqSerializer(), responses={200: serializer_class()})
    def put(self, request, *args, **kwargs):
        data = request.data
        account = request.user.account
        if data.get('name'):
            if models.NameChangeLog.objects.filter(account=account, created_at__gte=now().date()).exists():
                raise ValidateError('You can update profile only once a day.')
            models.NameChangeLog.objects.create(account=account, name=account.name)
            account.name = data['name']
        if 'avatar' in data:
            account.avatar = data['avatar']
        account.save()
        return Response(self.serializer_class(request.user.account).data)


class InWhitelistView(LoginMixin, APIView):

    @swagger_auto_schema(operation_description='是否在白名单', responses={200: '{"in_whitelist": false}'})
    def get(self, request, *args, **kwargs):
        return Response({'in_whitelist': models.WhitelistAddress.objects.filter(address=request.user.account.address).exists()})
