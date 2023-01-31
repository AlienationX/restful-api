
from django.db.backends.mysql.base import DatabaseWrapper as _DatabaseWrapper

class DatabaseWrapper(_DatabaseWrapper):
    def get_new_connection(self, conn_params):
        engine = self.settings_dict['SQLALCHEMY_ENGINE']
        return engine.raw_connection()