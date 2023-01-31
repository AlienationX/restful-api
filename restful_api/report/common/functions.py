import numpy as np

from restful_api.utils.timecycle import DatatimeUtils

def dataframe_to_dict(df):
    df = df.replace({np.nan: None})  # 返回的是null
    # df = df.replace({np.nan: ""})    # 返回空白，数字类型也会返回空白
    for col in df.columns:
        if df[col].dtype == "datetime64[ns]":
            df[col] = df[col].map(lambda x: DatatimeUtils.format_datetime(x))
    data = df.to_dict(orient='records')
    return data

def get_format_dict(cursor):
    columns = [col[0] for col in cursor.description]
    data_types = [col[1] for col in cursor.description]
    # schema_dict = dict(zip(columns, data_types))
    seq_type_dict = dict(enumerate(data_types))
    # print(schema_dict)
    # print(seq_type_dict)
    # for row in cursor.fetchall():
    #     tmp_row = []
    #     for index in range(len(seq_type_dict)):
    #         if seq_type_dict[index] == 12:
    #             print("format_datetime: ", DatatimeUtils.format_datetime(row[index]))   
    data = [
        dict(zip(columns, [DatatimeUtils.format_datetime(row[index]) if seq_type_dict[index] == 12 else row[index] for index in range(len(seq_type_dict))])) for row in cursor.fetchall()
    ]
    return data