from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import pagination, response


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    """
    A modified DRF's LimitOffsetPagination, which excludes any pagination metadata
    when returning the response.
    """

    def get_paginated_response(self, data):
        return response.Response(data)
