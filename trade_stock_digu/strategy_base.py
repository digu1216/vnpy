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
    def pick_stock(self):
        pass



class PickStockStrategyMa(PickStockBase):

    self.ma_greater = list() 
    self.ma_less = list()
    
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__()

    def pick_stock():            
        ds_tushare = DataServiceTushare()
        lst_code_picked = list()
        for ts_code in ds_tushare.lst_stock_:
            lst_stock_price = ds_tushare.getStockPriceInfo(ts_code, '20200218')
            for item in lst_stock_price:                
                if item['close'] >= item['high_500'] \
                        and item['close'] < item['low_250'] * 2\
                        and item['ma_60'] < item['ma_30']:
                    if item['ts_code'] not in self.list_stock_picked:
                        self.list_stock_picked.append(item['ts_code'])