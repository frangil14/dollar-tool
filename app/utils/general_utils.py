import json
from decimal import Decimal
import pandas as pd


def paginate_dataframe(dataframe, page_size, page_num):
    offset = page_size*(page_num-1)
    return dataframe[offset:offset + page_size]


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def parseTimestampToString(x):
    if pd.core.dtypes.common.is_datetime_or_timedelta_dtype(x):
        return x.dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return x


def parseStringToTimestamp(dataframe):
    if 'timestamp' in dataframe.columns:
        dataframe['timestamp'] = pd.to_datetime(
            dataframe['StartTime'], format="%Y-%m-%d %H:%M:%S")
    return dataframe


