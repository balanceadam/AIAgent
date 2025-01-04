from rest_framework import serializers

from account.serializers import AccountInfoSerializer
from assets import models


class AssetsChainModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetsChain
        fields = (
            'id', 'name', 'logo', 'fee', 'symbol'
        )


class FillingServiceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FillingService
        fields = (
            'id', 'name', 'logo', 'description'
        )


class AssetsGameModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetsGame
        fields = (
            'id', 'name', 'img', 'logo'
        )


class ProtocolModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Protocol
        exclude = ['is_enabled']


class AssetsTokenModelSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(read_only=True)
    chain = AssetsChainModelSerializer()
    filling_services = FillingServiceModelSerializer(many=True)
    games = AssetsGameModelSerializer(many=True)
    protocol = ProtocolModelSerializer()

    class Meta:
        model = models.AssetsToken
        exclude = ['is_enabled', 'sort']


class AssetsTokenValidateSerializer(serializers.Serializer):
    name = serializers.CharField()
    epal_name = serializers.CharField()
    ticker = serializers.CharField()


class AssetsTokenCreateSerializer(serializers.ModelSerializer):
    chain = serializers.PrimaryKeyRelatedField(queryset=models.AssetsChain.objects.all())
    filling_services = serializers.PrimaryKeyRelatedField(many=True, queryset=models.FillingService.objects.all())
    games = serializers.PrimaryKeyRelatedField(many=True, queryset=models.AssetsGame.objects.all())
    protocol = ProtocolModelSerializer()

    class Meta:
        model = models.AssetsToken
        exclude = ['created_at', 'updated_at', 'is_enabled', 'sort']

    def create(self, validated_data):
        protocol_data = validated_data.pop('protocol')
        protocol = models.Protocol.objects.create(**protocol_data)
        filling_services = validated_data.pop('filling_services')
        games = validated_data.pop('games')
        token = models.AssetsToken.objects.create(protocol=protocol, **validated_data)
        if filling_services:
            token.filling_services.set(filling_services)
        if games:
            token.games.set(games)
        return token


class AssetsTokenUpdateSerializer(serializers.ModelSerializer):
    # filling_services = serializers.PrimaryKeyRelatedField(many=True, queryset=models.FillingService.objects.all())
    games = serializers.PrimaryKeyRelatedField(many=True, queryset=models.AssetsGame.objects.all())

    class Meta:
        model = models.AssetsToken
        fields = ['telegram', 'website', 'twitter', 'labels', 'games']


class MarketDataReqSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class PositionModelSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(read_only=True)
    token = AssetsTokenModelSerializer()

    class Meta:
        model = models.Position
        exclude = ['is_enabled']


class PositionCreateSerializer(serializers.ModelSerializer):
    token = serializers.PrimaryKeyRelatedField(queryset=models.AssetsToken.objects.all())

    class Meta:
        model = models.Position
        exclude = ['created_at', 'updated_at', 'is_enabled']

    def create(self, validated_data):
        account = validated_data.pop('account')
        token = validated_data.pop('token')
        position = validated_data.pop('position')
        p, _ = models.Position.objects.get_or_create(account=account, token=token)
        p.position = position
        p.save()
        return p


class TransactionModelSerializer(serializers.ModelSerializer):
    account = AccountInfoSerializer()
    token = AssetsTokenModelSerializer()
    full_hash = serializers.CharField(source='hash')
    hash = serializers.CharField(source='format_hash')

    class Meta:
        model = models.Transaction
        exclude = ['is_enabled', 'created_at', 'updated_at']
