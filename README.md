# README

```shell
.venv/Scripts/activate
pip list

pip install -r requirement.txt
pip freeze > requirement.txt

pip install django
pip install djangorestframework

django-admin startproject restful_api
cd restful_api
django-admin startapp quickstart
django-admin startapp guard
django-admin startapp dataflow
django-admin startapp report
django-admin startapp lineage

# start
python manage.py runserver 8080
```

```shell
# 执行并创建数据库和表
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin

# 根据model生成数据库同步代码
python manage.py makemigrations polls
# 生成并显示sql语句
python manage.py sqlmigrate polls 0001
# 迭代和执行同步数据库代码
python manage.py migrate
```

```shell
# 进入shell命令行环境测试
python manage.py shell

# 测试 test.py 测试代码
python manage.py test polls
```

## deploy

```shell
nginx + gunicorn(linux)/uwsgi(linux+windows) + supervisor 
```

## database

```shell
pip install sqlalchemy
pip install pandans

pip install redis
pip install mysqlclient
pip install psycopg2
pip install pymssql
pip install cx_oracle
pip install pyhive, thrift, sasl, thrift-sasl
pip install impyla

pip install loguru
pip install arrow
pip install celery
```
