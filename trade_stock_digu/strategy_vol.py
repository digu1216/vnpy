from strategy_base import StrategyBase

class StrategyVol(StrategyBase):
    """
    股票池定义：
    1、流通市值小于500亿
    2、非st股票
    3、股价未暴涨，一年最高价/最低价 < 4
    4、多头排列 ma5>ma10>ma30>ma60>ma120>ma250>ma500,close>ma5,close<ma5*1.2
    按照量能在股票池中选股：
    1、统计股票池最近N=5日的每日换手率的前500排名得到集合A1-A5
    2、统计股票池最近N=5日的每日量比的前500排名得到集合B1-B5
    3、取A1-A5，B1-B5的交集得到买入股票
    策略调仓：
    1、每周调仓一次，卖出所有股票，平均买入新的买入股票

    """
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__()

    def pick_stock():    
        self.set_date(date)        
        ds_tushare = DataServiceTushare()
        lst_code_pool = list()
        lst_code_picked = list()
        for ts_code in ds_tushare.lst_stock_:
            lst_stock_price = ds_tushare.getStockPriceInfo(ts_code, self.stock_picked_date)
            for item in lst_stock_price:                
                if item['close'] >= item['high_500'] \
                        and item['close'] < item['low_250'] * 2\
                        and item['ma_60'] < item['ma_30']:
                    if item['ts_code'] not in self.list_stock_picked:
                        self.list_stock_picked.append(item['ts_code'])