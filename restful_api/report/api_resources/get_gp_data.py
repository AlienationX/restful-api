from rest_framework.viewsets import ViewSet
from django.http.response import JsonResponse
from loguru import logger
import pandas as pd

from restful_api.settings import GP_ENGINE
from ..common.functions import dataframe_to_dict


class Api(ViewSet):

    def list(self, request):
        df = pd.read_sql("select * from medical.dwb_master_info limit 23", con=GP_ENGINE)
        # df = df.replace({np.nan: None})
        data = dataframe_to_dict(df)
        # print(df.to_json(orient='records'))
        logger.info("it's ok...")
        return JsonResponse(data, safe=False)