from rest_framework import serializers

from account.serializers import AccountInfoSerializer
from social import models


class FollowReqSerializer(serializers.Serializer):
    account_id = serializers.IntegerField(required=False, allow_null=True)


class FollowResSerializer(serializers.Serializer):
    fans_count = serializers.IntegerField()
    following_count = serializers.IntegerField()


class FansModelSerializer(serializers.ModelSerializer):
    account = AccountInfoSerializer(read_only=True, source='follower')
    market_value = serializers.SerializerMethodField()
    has_token = serializers.SerializerMethodField()
    followed = serializers.SerializerMethodField()
    token_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Fans
        fields = ['id', 'account', 'has_token', 'market_value', 'followed', 'token_id']

    def get_market_value(self, obj):
        # view里实现
        return 0

    def get_has_token(self, obj):
        # view里实现
        return False

    def get_followed(self, obj):
        # view里实现
        return False

    def get_token_id(self, obj):
        # view里实现
        return 0


class FollowingsModelSerializer(FansModelSerializer):
    account = AccountInfoSerializer(read_only=True)


class CommentReqSerializer(serializers.Serializer):
    token_id = serializers.IntegerField()
    content = serializers.CharField(max_length=200)
    imgs = serializers.ListField(child=serializers.ImageField(), max_length=5, required=False, allow_empty=True, allow_null=True)


class CommentModelSerializer(serializers.ModelSerializer):
    account = AccountInfoSerializer()
    imgs = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ['id', 'account', 'content', 'imgs', 'created_at']

    def get_imgs(self, obj):
        # 在view处理
        return []
