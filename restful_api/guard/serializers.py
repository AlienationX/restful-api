from rest_framework import serializers
from .models import User, Group, UserGroups


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "joined_time"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserGroupsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserGroups
        fields = "__all__"
