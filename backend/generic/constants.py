class BaseType:
    CHOICES = ()

    @property
    def mapping(self):
        return dict(self.CHOICES)

    @property
    def reverse_mapping(self):
        return dict(zip(self.mapping.values(), self.mapping.keys()))

    @property
    def keys(self):
        return list(self.mapping.keys())


class BasicInfoType(BaseType):

    CHOICES = (
    )
