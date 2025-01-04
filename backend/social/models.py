from django.db import models

from generic.models import BaseModel
from generic.utils import get_time_str
from social import queryset


class Fans(BaseModel):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    follower = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='follower')
    objects = queryset.FollowQuerySet.as_manager()

    def __str__(self):
        return f'{self.follower} follows {self.account}'

    class Meta:
        unique_together = ('account', 'follower')
        verbose_name = 'Fans'
        verbose_name_plural = 'Fans'
        db_table = 'social_fans'
        ordering = ['-created_at']


class Comment(BaseModel):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    token = models.ForeignKey('assets.AssetsToken', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.account}-{self.token}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comment'
        db_table = 'social_comment'
        ordering = ('-created_at',)


def upload_comment_img(instance, filename):
    return f'social/comment/{instance.comment_id}/{get_time_str()}/{filename}'


class CommentImg(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=upload_comment_img)

    def __str__(self):
        return f'{self.comment_id}'

    class Meta:
        verbose_name = 'Comment Img'
        verbose_name_plural = 'Comment Img'
        db_table = 'social_comment_img'
        ordering = ('-created_at',)
