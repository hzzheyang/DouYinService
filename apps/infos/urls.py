# 定义视图处理的路由器
from django.conf.urls import url
from django.urls import path

from apps.infos.views import *

urlpatterns = [
    url(r'^author/local/$', SearchLocalAuthorView.as_view({'get': 'get'})),
    url(r'^author/douyin/$', SearchDouyinAuthorView.as_view({'get': 'get'})),

    url(r'^fans/local/$', GetLocalAuthorFansView.as_view({'get': 'get'})),
    url(r'^fans/douyin/$', GetDouyinAuthorFansView.as_view({'get': 'get'})),

    path('link/', link),
    path('send/', SendMessage.as_view()),

    path('to_sendmsg/', to_sendmsg),
    path('to_recmsg/', to_recmsg),
]