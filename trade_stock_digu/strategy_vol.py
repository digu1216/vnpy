from strategy_base import StrategyBase

class StrategyVol(StrategyBase):
    """
    成交量选股：
    1、统计最近N日换手率的排名
    2、统计最近N日量比的排名
    3、均线多头排列且估计没有暴涨过
    4、流通市值小于300亿
    """
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