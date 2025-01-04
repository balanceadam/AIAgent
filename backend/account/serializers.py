from rest_framework import serializers

from account import models


class AccountInfoReqSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    pw = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    avatar = serializers.ImageField(allow_null=True, required=False)


class AccountInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = models.Account
        fields = (
            'id', 'username', 'name', 'avatar', 'invite_code', 'created_at', 'updated_at'
        )
