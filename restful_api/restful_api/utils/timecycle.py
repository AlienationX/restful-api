import arrow

class DatatimeUtils:
    
    @staticmethod
    def format_datetime(dt):
        """ 去掉 pandas 的 datetime 类型存在T的问题 """
        if dt is None:
            return ""
        a = arrow.get(dt)
        dt_str = a.format("YYYY-MM-DD HH:mm:ss")
        return dt_str
    
class DateUtils:
    
    pass
