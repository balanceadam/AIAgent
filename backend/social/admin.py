from django.contrib import admin

from generic.admin import BaseModelAdmin
from social import models


@admin.register(models.Fans)
class FansAdmin(BaseModelAdmin):
    list_display = ('account', 'follower', 'created_at')
    autocomplete_fields = ['account', 'follower']
    search_fields = ['account__name', 'follower__name']


class CommentImgInline(admin.TabularInline):
    model = models.CommentImg


@admin.register(models.Comment)
class CommentAdmin(BaseModelAdmin):
    list_display = ('account', 'token', 'content', 'created_at')
    autocomplete_fields = ['account', 'token']
    search_fields = ['account__name', 'token__name']
    inlines = [CommentImgInline]
