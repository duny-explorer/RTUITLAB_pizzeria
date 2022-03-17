from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class OrderPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 20
    page_query_param = 'page'

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()

        return replace_query_param(url, self.page_query_param, page_number)
