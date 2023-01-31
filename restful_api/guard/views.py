from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import User, Group, UserGroups
from .serializers import UserSerializer, GroupSerializer, UserGroupsSerializer


# Create your views here.
class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupView(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserGroupsView(ModelViewSet):
    queryset = UserGroups.objects.all()
    serializer_class = UserGroupsSerializer
