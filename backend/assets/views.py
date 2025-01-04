import datetime

from django.utils.timezone import now
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.views import APIView, Response

from account.models import WhitelistAddress
from assets import models, serializers, filters
from generic.exceptions import ValidateError
from generic.views import LoginMixin, BaseAPIMixin


class AssetsChainListView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.AssetsChainModelSerializer
    queryset = models.AssetsChain.objects.filter(is_enabled=True)
    pagination_class = None


class FillingServiceListView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.FillingServiceModelSerializer
    queryset = models.FillingService.objects.filter(is_enabled=True)
    pagination_class = None


class AssetsGameListView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.AssetsGameModelSerializer
    queryset = models.AssetsGame.objects.filter(is_enabled=True)
    pagination_class = None


class AssetsTokenAllListView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.AssetsTokenModelSerializer
    filterset_class = filters.AssetsTokenFilter

    def get_queryset(self):
        return models.AssetsToken.objects.filter(is_enabled=True, protocol__isnull=False)


class AssetsTokenAllDetailView(BaseAPIMixin, generics.RetrieveAPIView):
    serializer_class = serializers.AssetsTokenModelSerializer

    def get_queryset(self):
        return models.AssetsToken.objects.filter(is_enabled=True, protocol__isnull=False)


def validate_token(account, data):
    if not WhitelistAddress.objects.filter(address=account.address).exists():
        raise ValidateError('Assets cannot be created if you are not in the whitelist.')
    if models.AssetsToken.objects.filter(account=account, protocol__isnull=False).count() >= account.token_count:
        raise ValidateError("Can't create another one.")
    if models.AssetsToken.objects.filter(name=data['name']).exists():
        raise ValidateError("The name already exists.")
    if models.AssetsToken.objects.filter(epal_name=data['epal_name']).exists():
        raise ValidateError("The epal name already exists.")
    if models.AssetsToken.objects.filter(ticker=data['ticker']).exists():
        raise ValidateError("The ticker already exists.")


class AssetsTokenValidateView(LoginMixin, APIView):
    serializer_class = serializers.AssetsTokenValidateSerializer

    @swagger_auto_schema(operation_description='创建token验证', request_body=serializer_class(), responses={200: '{"detail": "success"}'})
    def post(self, request, *args, **kwargs):
        self.get_data(request)
        validate_token(request.user.account, self.data)
        return Response({'detail': 'success'})


class AssetsTokenListCreateView(LoginMixin, generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AssetsTokenCreateSerializer
        return serializers.AssetsTokenModelSerializer

    def get_queryset(self):
        return models.AssetsToken.objects.filter(
            is_enabled=True, account=self.request.user.account, protocol__isnull=False
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_token(self.request.user.account, serializer.validated_data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)


class AssetsTokenDetailView(LoginMixin, generics.RetrieveUpdateAPIView):
    def get_queryset(self):
        return models.AssetsToken.objects.filter(account=self.request.user.account)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.AssetsTokenUpdateSerializer
        return serializers.AssetsTokenModelSerializer


class MinuteMarketDataView(BaseAPIMixin, APIView):
    serializer_class = serializers.MarketDataReqSerializer

    @swagger_auto_schema(operation_description='分钟行情数据', query_serializer=serializer_class(), responses={200: '[[1, 2, 3, 4, 5]]'})
    def get(self, request, *args, **kwargs):
        self.get_query_params(request)
        # time_now = now()
        # data = models.MinuteMarketData.objects.filter(
        #     protocol_id=self.data['protocol_id'], time__gt=time_now-datetime.timedelta(hours=3)
        # ).order_by('-time')
        # TODO: 先用假数据
        data = models.MinuteMarketData.objects.filter(protocol_id=self.data['id']).order_by('-time')[:300]
        # data = models.MinuteMarketData.objects.order_by('-time')[:150]
        results = []
        for d in data:
            results.append([d.time.timestamp(), d.open, d.high, d.low, d.close])
        results.reverse()
        return Response(results)


class PositionsView(LoginMixin, generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PositionCreateSerializer
        return serializers.PositionModelSerializer

    def get_queryset(self):
        return models.Position.objects.filter(is_enabled=True, account=self.request.user.account)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)


class TransactionsView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.TransactionModelSerializer
    queryset = models.Transaction.objects.filter(is_enabled=True)
    filterset_class = filters.TransactionsFilter
