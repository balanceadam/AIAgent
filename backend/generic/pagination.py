from rest_framework.pagination import PageNumberPagination, NotFound


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view=view)
        except NotFound:
            page_size = self.get_page_size(request)
            paginator = self.django_paginator_class(queryset, page_size)
            self.page = paginator.page(1)
            self.request = request
            return []
