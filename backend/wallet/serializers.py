from rest_framework import serializers


class WalletLoginOrRegisterReqSerializer(serializers.Serializer):
    address = serializers.CharField()
    chain_id = serializers.CharField()
