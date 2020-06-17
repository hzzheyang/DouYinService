from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class AuthorPageNumberPagination(PageNumberPagination):
    # ?page=页码  定义代表页码的属性，如果写pages,就是?pages=页码
    page_query_param = 'page'
    # ?page=页码 设置默认下一页显示的条数
    page_size = 22
    # ?page=页码&page_size=条数 用户自定义一页显示的条数
    page_size_query_param = 'page_size'
    # 用户自定义一页显示的条数最大限制：数值超过5也只显示5条
    max_page_size = 22

    def get_paginated_response(self, data):
        """输出格式"""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),  # 整个数据的个数
            ('msg', 'success'),  # 验证消息
            ('status', 0),
            ('next', self.get_next_link()),  # 下一页url
            ('previous', self.get_previous_link()),  # 上一页url
            ('results', data)  # 当前页的数据
        ]))

