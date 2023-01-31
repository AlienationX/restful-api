from rest_framework.viewsets import ViewSet
from django.http.response import JsonResponse
import pandas as pd

from restful_api.settings import MYSQL_ENGINE
from ..common.functions import dataframe_to_dict

class Api(ViewSet):

    def list(self, request):
        df = pd.read_sql("select * from test.example", con=MYSQL_ENGINE)
        # df = df.replace({np.nan: None})
        data = dataframe_to_dict(df)
        # print(df.to_json(orient='records'))
        return JsonResponse(data, safe=False)

