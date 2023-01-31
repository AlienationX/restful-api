from django.urls import path, include
from rest_framework import routers
from loguru import logger

from . import views

# 注册的接口才会在 rest framework root api 页面显示
# 只有继承APIView即可被接口文档识别，只有ViewSet才能注册

# base_name 用于创建的 URL 名称的基础。
# 如果未设置，basename 将根据视图集的 queryset 属性 (如果它有的话) 自动生成。
# 注意，如果视图集不包含 queryset 属性，那么在注册视图集时必须设置 base_name。

# DefaultRouter 比 SimpleRouter 多了个 root api 页面
router = routers.DefaultRouter()

router.register(r'example', views.ExampleViewSet, basename="example")
router.register(r'example_sql', views.ExampleSQLViewSet, basename="example_sql")

# AssertionError: 'ExampleModelViewSet' should either include a `queryset` attribute, or override the `get_queryset()` method.
# router.register(r'example_model_view_set', example.ExampleModelViewSet, basename="example_model_view_set")

def auto_register(router, folder="api_resources", exclude=["__init__"]):
    from pathlib import Path
    api_folder = "api_resources"
    api_path = Path(__file__).parent.joinpath(api_folder)
    logger.info(api_path)
    for path in api_path.iterdir():
        file_name, file_type = path.stem, path.suffix
        if not path.is_file() or file_name == "__init__" or file_type != ".py":
            continue
        resource = file_name
        model_str = "{}.{}".format(api_folder, resource)
        logger.info("model_str: " + model_str)
        # model_name = __import__(model_str, globals(), locals(), "Api")
        model_name = __import__(model_str, globals(), locals(), fromlist=[resource], level=1)
        router.register(api_folder + "/" + resource, model_name.Api, basename=resource)
    return router

router = auto_register(router)

app_name = 'report'
urlpatterns = [
    # ex: /report/
    path('', include(router.urls)),
    path('raw_example/', views.ExampleView.as_view()),
    path('raw_example_json/', views.ExampleJsonView.as_view()),
    path('raw_example_api/', views.ExampleAPIView.as_view()),
    path('raw_example_sql/', views.ExampleSQLAPIView.as_view()),
]

# path('', include(router.urls))  等同  urlpatterns += router.urls
