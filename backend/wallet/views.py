from drf_yasg2.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from account.utils import get_token_by_user, create_account
from generic.exceptions import ValidateError
from generic.views import BaseAPIMixin, LoginMixin
from wallet import models, serializers


class WalletLoginOrRegisterView(BaseAPIMixin, APIView):
    serializer_class = serializers.WalletLoginOrRegisterReqSerializer

    @swagger_auto_schema(operation_description='钱包注册或登录', request_body=serializer_class(), responses={200: '{"token": ""}'})
    def post(self, request):
        self.get_data(request)
        chain_id = self.data.get('chain_id')
        address = self.data.get('address')

        network, _ = models.Network.objects.get_or_create(chain_id=chain_id)
        wallet_address = models.WalletAddress.objects.filter(address=address).first()
        if wallet_address:
            if not models.WalletAddress.objects.filter(address=address, network=network).exists():
                models.WalletAddress.objects.create(address=address, network=network, account=wallet_address.account)
            return Response({'token': get_token_by_user(wallet_address.account.user)})
        account = create_account(address)
        models.WalletAddress.objects.create(
            account=account, network=network, address=address
        )
        return Response({'token': get_token_by_user(account.user)})
