from django.db import models


class FollowQuerySet(models.query.QuerySet):
    def followed(self, account, follower):
        return self.filter(account=account, follower=follower).exists()
