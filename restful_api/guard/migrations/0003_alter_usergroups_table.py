# Generated by Django 4.1.4 on 2022-12-30 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guard', '0002_alter_group_group_name_alter_user_joined_time_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='usergroups',
            table='user_groups',
        ),
    ]
