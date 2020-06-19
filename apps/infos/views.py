import json
import time
from pprint import pprint
import urllib3
from django.shortcuts import render, HttpResponse  # 引入HttpResponse
from django.views import View
from dwebsocket.decorators import accept_websocket  # 引入dwbsocket的accept_websocket装饰器
import uuid
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from Tools.DouyinTools import DouYinTools
from apps.infos import pagenations
from . import models, serializers

urllib3.disable_warnings()


class SearchLocalAuthorView(ListModelMixin, RetrieveModelMixin,
                            CreateModelMixin, ViewSetMixin, GenericAPIView):
    queryset = models.Author.objects.filter(is_delete=False)
    serializer_class = serializers.AuthorSerializer
    lookup_field = 'pk'  # 先定义好，单查可以使用，默认是pk  自定义主键的有名分组，如果路由有名分组
    # 分页组件指定
    pagination_class = pagenations.AuthorPageNumberPagination
    # 局部配置 过滤类 们（全局配置用DEFAULT_FILTER_BACKENDS）
    filter_backends = [SearchFilter, OrderingFilter]
    # 第三步：SearchFilter过滤类依赖的过滤条件 => 接口：/xx/?search=...
    search_fields = ['author_name']  # 筛选字段
    # OrderingFilter过滤类依赖的过滤条件 -> 接口: /xx/?ordering=排序字段，排序字段前面加 - 等于反序，多字段用 ， 隔开
    ordering_fields = ['author_fans_num', 'author_favorited', 'author_aweme_count']

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    def get_fans_list(self, author_id, fan_psc):
        a = models.Author.objects.get(id=author_id)
        b = a.employee.filter(fan_is_follow=0)[0: int(fan_psc)]
        return b

    def post(self, request, *args, **kwargs):
        request_data = request.data
        data = self.get_fans_list(141, 10)
        return Response({
            'status': 1,
            'msg': 'b'
        })


class SearchDouyinAuthorView(ListModelMixin, RetrieveModelMixin,
                             CreateModelMixin, ViewSetMixin, GenericAPIView):
    queryset = models.Author.objects.filter(is_delete=False)
    serializer_class = serializers.AuthorSerializer
    lookup_field = 'pk'  # 先定义好，单查可以使用，默认是pk  自定义主键的有名分组，如果路由有名分组

    def get(self, request, *args, **kwargs):
        keyinput = request.GET.get('keyinput')
        curosr = request.GET.get('curosr')

        Douyin = DouYinTools()
        user_data = Douyin.get_global_search_data(keyinput, int(curosr))
        if user_data['status'] == 0:
            return Response({
                'status': 0,
                'msg': 'success search douyin author',
                'results': user_data['results']['user_list']
            })
        elif user_data['status'] == 1:
            return Response({
                'status': 1,
                'msg': '抖音爬虫发生错误',
                'results': ''
            })

    @staticmethod
    def get_actor_ids(request_data, many):
        id_list = []
        for actor_name in request_data['actor_name']:
            if models.Fans.objects.filter(actor_name=actor_name):
                id = models.Fans.objects.filter(actor_name=actor_name).first()
                id_list.append(id)
            else:
                data = {"actor_name": actor_name}
                actor_ser = serializers.FansSerializer(data=data, many=many)
                actor_ser.is_valid(raise_exception=True)
                actor_result = actor_ser.save()
                id_list.append(serializers.FansSerializer(actor_result, many=many).data['id'])

        return id_list

    def post(self, request, *args, **kwargs):
        request_data = request.data
        fan_psc = int(request_data['fan_psc'])
        if isinstance(request_data['authors'], dict):  # 判断获取的数据是否是dict
            many = False
        elif isinstance(request_data['authors'], list):  # 判断获取的数据是否是list
            many = True
        else:
            return Response({
                'status': 1,
                'msg': '数据错误'
            })

        # 反序列化
        movie_ser = serializers.AuthorSerializer(data=request_data['authors'], many=many)
        # 校验数据，和检测作者是否存在
        movie_ser.is_valid(raise_exception=True)
        actor_result = movie_ser.save()
        for author in actor_result:
            id = author.id
            author_uid = author.author_sec_uid
            author_sec_uid = author.author_sec_uid
            obj = DouYinTools()
            min_time = time.time()
            while True:
                fans_data = obj.get_fans_list(author_uid, author_sec_uid, min_time, fan_psc, id)
                if len(fans_data['fans_list']) > 0:
                    min_time = fans_data['min_time']
                    if isinstance(fans_data['fans_list'], dict):  # 判断获取的数据是否是dict
                        many = False
                    elif isinstance(fans_data['fans_list'], list):  # 判断获取的数据是否是list
                        many = True
                    else:
                        return Response({
                            'status': 1,
                            'msg': '数据错误'
                        })
                    fan_ser = serializers.FansSerializer(data=fans_data['fans_list'], many=many)
                    fan_ser.is_valid(raise_exception=True)
                    fan_result = fan_ser.save()
                    fan_psc -= len(fan_result)
                    if fan_psc == 0:
                        fan_psc = int(request_data['fan_psc'])
                        min_time = time.time()
                        break

                    elif fan_psc != 0:
                        pass
                else:
                    return Response({
                        'status': 1,
                        'msg': {'code': 101, 'message': '爬虫爬取超过上限,请联系管理员'}
                    })

        return Response({
            'status': 1,
            'msg': {'code': 0, 'message': '爬取粉丝完毕'}
        })


class GetLocalAuthorFansView(ListModelMixin, RetrieveModelMixin,
                             CreateModelMixin, ViewSetMixin, GenericAPIView):
    queryset = models.Fans.objects.filter(is_delete=False)
    serializer_class = serializers.FansSerializer
    lookup_field = 'pk'  # 先定义好，单查可以使用，默认是pk  自定义主键的有名分组，如果路由有名分组

    def get(self, request, *args, **kwargs):
        author_id = models.Author.objects.get(author_uid=int(request.GET.get('uid'))).id
        # fans=作者id
        list_info = models.Fans.objects.filter(fans=int(author_id))
        fans_dict = {
            'fans_list': []
        }
        for info in list_info:
            fan_uid = info.fan_uid
            fan_name = info.fan_name
            fans_dict['fans_list'].append({'fan_uid': fan_uid, 'fan_name':fan_name})

        return Response({
            'status': 0,
            'msg': 'success get loacl fans info',
            'results': fans_dict
        })


class GetDouyinAuthorFansView(ListModelMixin, RetrieveModelMixin,
                              CreateModelMixin, ViewSetMixin, GenericAPIView):
    queryset = models.Fans.objects.filter(is_delete=False)
    serializer_class = serializers.FansSerializer
    lookup_field = 'pk'  # 先定义好，单查可以使用，默认是pk  自定义主键的有名分组，如果路由有名分组

    def get(self, request, *args, **kwargs):
        uid = request.GET.get('uid')
        sec_id = request.GET.get('sec_id')
        max_time = request.GET.get('max_time')
        obj = DouYinTools()
        data = obj.get_fans_list(uid, sec_id, max_time)

        return Response({
            'status': 0,
            'msg': 'success get douyin fans info',
            'results': json.loads(data)
        })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):  # 判断获取的数据是否是dict
            many = False
        elif isinstance(request_data, list):  # 判断获取的数据是否是list
            many = True
        else:
            return Response({
                'status': 1,
                'msg': '数据错误'
            })

        # 反序列化
        fans_ser = serializers.FansSerializer(data=request_data, many=many)
        # 校验数据，和检测作者是否存在
        fans_ser.is_valid(raise_exception=True)
        fans_ser.save()

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': 'success add fans'
        })



def to_sendmsg(request):
    return render(request, 'sendmsg.html')


def to_recmsg(request):
    return render(request, 'recmsg.html')


clients = {}  # 创建客户端列表，存储所有在线客户端


# 允许接受ws请求
@accept_websocket
def link(request):
    # 判断是不是ws请求
    if request.is_websocket():
        userid = str(uuid.uuid1())
        # 判断是否有客户端发来消息，若有则进行处理，若发来“test”表示客户端与服务器建立链接成功
        while True:
            message = request.websocket.wait()
            if not message:
                break
            else:
                nike_id = json.loads(message)['userId']
                # 保存客户端的ws对象，以便给客户端发送消息,每个客户端分配一个唯一标识
                clients[nike_id] = request.websocket
                pprint(clients)

def send(request):
    # 获取消息
    msg=request.POST.get("msg")
    # 获取到当前所有在线客户端，即clients
    # 遍历给所有客户端推送消息
    for client in clients:
        clients[client].send(msg.encode('utf-8'))
    return HttpResponse({"msg":"success"})


class SendMessage(GenericAPIView):
    def post(self, request, *args, **kwargs):
        request_data = request.data
        msg = request_data['msg']
        phone_key = request_data['phone_key']
        pprint('phone_key: {}'.format(phone_key))

        for phone_local_key, send_obj in clients.items():
            if str(phone_local_key) == str(phone_key):
                send_obj.send(json.dumps({'status': 0, 'msg': msg}))

        return Response({
            'status': 'success',
            'msg': {'code': 0, 'message': '发送成功'}
        })