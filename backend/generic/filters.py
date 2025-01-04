from django_filters import rest_framework as filters

from generic import models, constants


class BasicInfoFilter(filters.FilterSet):
    type = filters.ChoiceFilter(choices=constants.BasicInfoType.CHOICES, field_name='type')

    class Meta:
        model = models.BasicInfo
        fields = ['type', 'name']
