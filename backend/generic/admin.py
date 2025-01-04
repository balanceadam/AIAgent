import datetime
from django import forms
from django.contrib import admin, messages
from django.contrib.admin import widgets
from django.contrib.admin.options import get_ul_class
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.core.exceptions import FieldDoesNotExist
from import_export.admin import ExportMixin

from generic import models

admin.site.site_header = 'project-e'
admin.site.site_title = 'project-e'


class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = 20
    logic_delete = False

    def get_fields(self, request, obj=None):
        if not self.fields:
            return super().get_fields(request, obj)
        fields = self.fields.copy()
        return fields

    def _formfield_for_foreignkey(self, qs, db_field, request):
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        db = kwargs.get('using')

        if 'widget' not in kwargs:
            if db_field.name in self.get_autocomplete_fields(request):
                kwargs['widget'] = AutocompleteSelect(db_field, self.admin_site, using=db)
            elif db_field.name in self.raw_id_fields:
                kwargs['widget'] = widgets.ForeignKeyRawIdWidget(db_field.remote_field, self.admin_site, using=db)
            elif db_field.name in self.radio_fields:
                kwargs['widget'] = widgets.AdminRadioSelect(attrs={
                    'class': get_ul_class(self.radio_fields[db_field.name]),
                })
                kwargs['empty_label'] = _('None') if db_field.blank else None

        if 'queryset' not in kwargs:
            queryset = self.get_field_queryset(db, db_field, request)
            if queryset is not None:
                if hasattr(queryset.model, 'is_enabled'):
                    queryset = queryset.filter(is_enabled=True)
                kwargs['queryset'] = self._formfield_for_foreignkey(queryset, db_field, request)
        return db_field.formfield(**kwargs)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        # if 'autocomplete' in request.path:
        #     queryset = self.get_queryset(request)
        return queryset, use_distinct

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        if self.logic_delete:
            self.model.objects.filter(id=obj.id).update(is_enabled=0, updated_at=now())
        else:
            obj.delete()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        if self.logic_delete:
            try:
                queryset.model._meta.get_field('is_enabled')
                queryset.update(is_enabled=0, updated_at=now())
            except FieldDoesNotExist:
                # Handle the case where the field does not exist if needed
                pass
        else:
            queryset.delete()

    def get_queryset(self, request):
        """Only display data where is_enabled=True."""
        qs = super().get_queryset(request)

        try:
            qs.model._meta.get_field('is_enabled')
            return qs.filter(is_enabled=True)
        except FieldDoesNotExist:
            return qs


@admin.register(models.RequestLog)
class RequestLogAdmin(BaseModelAdmin):
    list_display = ['id', 'trade_id', 'service', 'url', 'request_at', 'response_at']
    list_filter = ['service']
    search_fields = ['trade_id', 'service']
    fields = ['trade_id', 'service', 'url', 'request_at', 'response_at']


@admin.register(models.RequestLogDetail)
class RequestLogDetailAdmin(BaseModelAdmin):
    list_display = ['id', 'log', 'request', 'response']
    list_filter = ['log__service']
    search_fields = ['log__trade_id', 'log__service']
    fields = ['log', 'request', 'response']
    autocomplete_fields = ['log']


@admin.register(models.BasicInfo)
class BasicInfoAdmin(BaseModelAdmin):
    list_display = ['id', 'type', 'name', 'value', 'is_enabled', 'updated_at']
    list_filter = ['type', 'created_at']
    search_fields = ['name']
    fields = ['type', 'name', 'value', 'is_enabled']
    ordering = ['type', '-created_at']
