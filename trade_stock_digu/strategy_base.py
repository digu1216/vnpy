from datetime import datetime
from abc import ABC, abstractmethod

from logger import Logger
from convert_utils import string_to_datetime, time_to_str

class StrategyBase(ABC):
    """
    选股策略基类
    """
    author = ""
    logger = Logger().getlog()

    def __init__(self):
        """Constructor"""               
        self.lst_stock_picked = list()
        self.stock_picked_date = time_to_str(datetime.now(), '%Y%m%d')
    
    def set_date(self, date):
        # 设置选股日期
        self.stock_picked_date = date

    @abstractmethod
    def pick_stock(self, date):
        pass

