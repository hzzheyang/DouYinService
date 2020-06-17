# 定义视图处理的路由器
from django.conf.urls import url
from apps.infos.views import SearchLocalAuthorView, SearchDouyinAuthorView, GetLocalAuthorFansView, \
    GetDouyinAuthorFansView

urlpatterns = [
    url(r'^author/local/$', SearchLocalAuthorView.as_view({'get': 'get'})),
    url(r'^author/douyin/$', SearchDouyinAuthorView.as_view({'get': 'get'})),

    url(r'^fans/local/$', GetLocalAuthorFansView.as_view({'get': 'get'})),
    url(r'^fans/douyin/$', GetDouyinAuthorFansView.as_view({'get': 'get'})),

]
