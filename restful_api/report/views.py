from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views import View
from django.views.generic.base import View
from django.core import serializers
from django.db import connection, connections
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet, ViewSetMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import json

from restful_api.utils.timecycle import DatatimeUtils


class ExampleView(View):
    # 接口文档都不显示
    def get(self, request):
        return HttpResponse(json.dumps({'some': 'data'}))

class ExampleJsonView(View):
    # 接口文档都不显示
    def get(self, request):
        # return HttpResponse(json.dumps(data), content_type='application/json')
        # list_data = ["张三", "25", "19000347", "上呼吸道感染"]
        # return JsonResponse(list_data, safe=False)
        # 为了对 dict 以外的对象进行序列化，你必须将 safe 参数设置为 False：
        return JsonResponse({'some': 'data'})

class ExampleAPIView(APIView):
    # rdf root 首页不显示
    # docs 显示
    # swagger 显示
    def get(self, request):
        return Response({'some': 'data'})

class ExampleSQLAPIView(APIView):
    # 接口文档都不显示
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("select * from auth_user")
        with connections["auth_db"].cursor() as cursor:
            cursor.execute("select t.*, 99.9 as fee, cast(99.9 as decimal(38,4)) as fee1, 100 as ord from information_schema.tables t limit 23")
            # print(cursor.description)
            # columns = [col[0] for col in cursor.description]
            # data = [
            #     dict(zip(columns, row)) for row in cursor.fetchall()
            # ]
            from .common.functions import get_format_dict
            data = get_format_dict(cursor)
        # with connections["warehouse"].cursor() as cursor:
        #     cursor.execute("select table_catalog, table_schema, table_name, table_type from information_schema.tables")
        #     columns = [col[0] for col in cursor.description]
        #     data = [
        #         dict(zip(columns, row))
        #         for row in cursor.fetchall()
        #     ]
        return JsonResponse(data, safe=False)

class ExampleViewSet(ViewSet):
    """强烈推荐，想实现某个接口直接添加即可"""
    def list(self, request):
        """ 获取所有data """
        return Response({'some': 'data'})

    def create(self, request):
        """
        :param request:
        :return:
        """
        return Response({'some': 'data'})

    # def retrieve(self, request, pk):
    #     return Response({'some': 'data', 'pk': pk})

    def update(self, request, pk):
        return Response({'some': 'data', 'pk': pk})

    def destroy(self, request, pk):
        return Response({'some': 'data', 'pk': pk})

class ExampleModelViewSet(ModelViewSet):
    # '''终极ModelViewSet'''
    # serializer_class = Bookserializer
    # queryset = Book.objects.all()

    # # 以上代码 实现了普通的增删改查
    # # 定义自己的方法
    # @action(methods=['get'], detail=False)
    # # action 解决路由问题 用DefaultRouter生成标准路由
    # def latest(self, request):
    #     '''自定义的方法'''
    #     book = Book.objects.latest('id')
    #     serializer = self.get_serializer(book)
    #     return Response(serializer.data)

    def get(self, request):
        return Response({'some': 'data'})

class ExampleSQLViewSet(ViewSet):

    def list(self, request):
        """
        create table example (
            id int,
            name varchar(100),
            sex char(1),
            age int,
            address text,
            fee double,
            fee1 float,
            fee2 decimal(38,4),  -- 会识别成字符串
            dt date,
            dt1 datetime,        -- 2023-01-06T16:56:27 会默认增加 T
            dt2 timestamp        -- 2023-01-06T16:56:27
        );

        insert into example values (1, 'aaa', 'F', 12, 'beijing上海', 88.8, 88.8, 88.8, date(now()), now(), now());
        """
        with connections["auth_db"].cursor() as cursor:
            cursor.execute("select * from test.example")
            # print(cursor.description)
            columns = [col[0] for col in cursor.description]
            data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        # with connections["warehouse"].cursor() as cursor:
        #     cursor.execute("select table_catalog, table_schema, table_name, table_type from information_schema.tables")
        #     columns = [col[0] for col in cursor.description]
        #     data = [
        #         dict(zip(columns, row))
        #         for row in cursor.fetchall()
        #     ]
        return JsonResponse(data, safe=False)