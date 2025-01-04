from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from drf_yasg2.utils import swagger_auto_schema

from account.models import Account
from assets.models import AssetsToken
from generic.exceptions import ValidateError
from generic.views import LoginMixin, BaseAPIMixin
from social import models, serializers, filters


class FollowView(BaseAPIMixin, APIView):
    serializer_class = serializers.FollowReqSerializer

    @swagger_auto_schema(operation_description='获取关注&粉丝数量', responses={200: serializers.FollowResSerializer()})
    def get(self, request, *args, **kwargs):
        self.get_query_params(request)
        if not self.data.get('account_id'):
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            return Response({
                'fans_count': models.Fans.objects.filter(account=request.user.account).count(),
                'following_count': models.Fans.objects.filter(follower=request.user.account).count(),
            })
        return Response({
            'fans_count': models.Fans.objects.filter(account_id=self.data['account_id']).count(),
            'following_count': models.Fans.objects.filter(follower_id=self.data['account_id']).count(),
        })

    @swagger_auto_schema(operation_description='关注', request_body=serializer_class, responses={200: '{"detail":"success"}'})
    def post(self, request):
        self.get_data(request)
        if request.user.account.id == self.data['account_id']:
            raise ValidateError('You cannot follow yourself')
        account = Account.objects.filter(id=self.data['account_id']).first()
        if not account:
            raise ValidateError('Account not found')
        models.Fans.objects.get_or_create(account=account, follower=request.user.account)
        return Response({'detail': 'success'})

    @swagger_auto_schema(operation_description='取消关注', request_body=serializer_class, responses={200: '{"detail":"success"}'})
    def delete(self, request):
        self.get_data(request)
        fans = models.Fans.objects.filter(account_id=self.data['account_id'], follower=request.user.account)
        if fans.exists():
            fans.delete()
        return Response({'detail': 'success'})


class FollowedView(LoginMixin, APIView):
    serializer_class = serializers.FollowReqSerializer

    @swagger_auto_schema(
        operation_description='是否关注某个用户', query_serializer=serializer_class(),
        responses={200: '{"followed": true}'}
    )
    def get(self, request, *args, **kwargs):
        self.get_query_params(request)
        account = generics.get_object_or_404(Account, id=self.data['account_id'])
        return Response({
            'followed': models.Fans.objects.followed(account, request.user.account)
        })


class FansView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.FansModelSerializer
    filterset_class = filters.FansFilter

    def get_queryset(self, *args, **kwargs):
        if not self.request.query_params.get('accountId'):
            if not self.request.user.is_authenticated:
                raise AuthenticationFailed()
            return models.Fans.objects.filter(account=self.request.user.account)
        return models.Fans.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data

        account_ids = []
        for d in data:
            account_ids.append(d.get('account').get('id'))
        tokens = AssetsToken.objects.filter(account_id__in=account_ids, protocol__isnull=False)
        market_value_mapping = {}
        token_id_mapping = {}
        has_token_mapping = {}
        for token in tokens:
            if token.protocol:
                market_value_mapping[token.account_id] = token.protocol.market_value
                has_token_mapping[token.account_id] = True
                token_id_mapping[token.account_id] = token.id
        for d in data:
            d['market_value'] = market_value_mapping.get(d.get('account').get('id'))
            d['has_token'] = bool(has_token_mapping.get(d.get('account').get('id')))
            d['token_id'] = token_id_mapping.get(d.get('account').get('id'))

        if request.user.is_authenticated:
            fans = models.Fans.objects.filter(follower=request.user.account, account_id__in=account_ids)
            fans_mapping = {}
            for f in fans:
                fans_mapping[f.account.id] = True
            for d in data:
                d['followed'] = bool(fans_mapping.get(d.get('account').get('id')))
        return self.get_paginated_response(data)


class FollowingsView(FansView):
    serializer_class = serializers.FollowingsModelSerializer
    filterset_class = filters.FollowingsFilter

    def get_queryset(self, *args, **kwargs):
        if not self.request.query_params.get('accountId'):
            if not self.request.user.is_authenticated:
                raise AuthenticationFailed()
            return models.Fans.objects.filter(follower=self.request.user.account)
        return models.Fans.objects.all()


class CommentListCreateView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.CommentModelSerializer
    queryset = models.Comment.objects.filter(is_enabled=True)
    filterset_class = filters.CommentFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data

        comment_ids = []
        for d in data:
            comment_ids.append(d.get('id'))
        imgs = models.CommentImg.objects.filter(comment_id__in=comment_ids)
        img_mapping = {}
        for img in imgs:
            if img.comment_id in img_mapping:
                img_mapping[img.comment_id].append(img.img.url)
            else:
                img_mapping[img.comment_id] = [img.img.url]
        for d in data:
            d['imgs'] = img_mapping.get(d.get('id')) or []

        return self.get_paginated_response(data)

    @swagger_auto_schema(operation_description='添加评论', request_body=serializers.CommentReqSerializer, responses={200: '{"detail":"success"}'})
    def post(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed()
        self.serializer_class = serializers.CommentReqSerializer
        self.get_data(request)
        token = AssetsToken.objects.filter(id=self.data['token_id']).first()
        if not token:
            raise ValidateError('Token not found')
        comment = models.Comment.objects.create(
            account=request.user.account, token_id=self.data['token_id'], content=self.data['content']
        )
        if self.data.get('imgs'):
            imgs = []
            for img in self.data['imgs']:
                imgs.append(models.CommentImg(comment=comment, img=img))
            models.CommentImg.objects.bulk_create(imgs)
        return Response({'detail': 'success'})


class CommentDeleteView(LoginMixin, generics.DestroyAPIView):
    def get_queryset(self):
        return models.Comment.objects.filter(account=self.request.user.account)
