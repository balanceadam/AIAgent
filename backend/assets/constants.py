from generic.constants import BaseType


class AssetsTokenInitialBuyType(BaseType):
    FEE = 1
    AMOUNT = 2

    CHOICES = (
        (FEE, 'Fee'),
        (AMOUNT, 'Amount'),
    )
