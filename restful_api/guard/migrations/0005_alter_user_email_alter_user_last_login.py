# Generated by Django 4.1.4 on 2022-12-30 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guard', '0004_alter_usergroups_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=64, verbose_name='电子邮箱'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login datetime'),
        ),
    ]
