from import_export import resources

from account import models


class WhitelistAddressResource(resources.ModelResource):

    class Meta:
        model = models.WhitelistAddress
        fields = ('address', 'batch')
        exclude = ('id',)
        import_id_fields = []
