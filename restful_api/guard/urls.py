from django.urls import path, include

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserView)
router.register(r'groups', views.GroupView)
router.register(r'user_groups', views.UserGroupsView)

app_name = 'guard'
urlpatterns = [
    # ex: /guard/
    path('', include(router.urls)),
]