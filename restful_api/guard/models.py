from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, null=False, unique=True)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64, verbose_name="电子邮箱")
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    joined_time = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField('last login datetime', null=True)


class Group(models.Model):
    group_name = models.CharField(max_length=32, null=False, unique=True)
    desc = models.CharField("描述", max_length=64)


class UserGroups(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = "guard_user_groups"


# class Permissions(models.Model):
#     pass
#
# class GroupPermissions(models.Model):
#     pass
#
# class UserPermissions(models.Model):
#     pass
