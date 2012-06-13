from bean import BeanManager as BM
from datetime import datetime,timedelta
import re

from timeutility import get_range_from_string

class GRGManager(object):
    def __getattr__(self,attr):
        def wrapper(**kwargs):
            if re.match("show_.+" , attr):
                _ , what = attr.split("_")
                time = kwargs["time"]
                random = kwargs["random"]

                from_t,to_t = get_range_from_string(time)
                
                kwargs = {
                    "bt":what,
                    "when_created":{
                        "$gt":from_t,
                        "$lt":to_t
                    }
                }
                return BM.get_beans(kwargs)

        return wrapper

class GRGFormatter(object):
    pass
