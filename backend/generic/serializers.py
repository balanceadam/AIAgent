from rest_framework import serializers

from generic import models


class BasicInfoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BasicInfo
        fields = ('id', 'type', 'name', 'value', 'created_at', 'updated_at')
