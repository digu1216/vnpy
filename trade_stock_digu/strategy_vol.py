import numpy as np
from strategy_base import StrategyBase

class StrategyVol(StrategyBase):
    """
    股票池定义：
    1、流通市值小于500亿
    2、选股当天自由流通股换手率>1%
    3、股价未暴涨，一年最高价/最低价 < 4
    4、多头排列 ma5>ma20>ma60>ma120>ma250,close>ma5,close<ma5*1.2
    按照量能在股票池中选股：
    1、统计股票池最近N=5日的每日换手率的前500排名得到集合A1-A5
    2、统计股票池最近N=5日的每日量比的前500排名得到集合B1-B5
    3、取A1-A5，B1-B5的交集得到买入股票
    策略调仓：
    1、每周调仓一次，卖出所有股票，平均买入新的买入股票
    """
    circ_mv_max = 5000000
    turnover_rate_f_min = 0.01
    pct_chg_max_year = 4.0
    n_days = 5
    pct_close_to_ma5 = 1.2
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__()

    def pick_stock():    
        self.set_date(date)        
        ds_tushare = DataServiceTushare()
        lst_code_pool = list()
        lst_code_picked = list()
        for ts_code in ds_tushare.lst_stock_:
            dic_stock_price = ds_tushare.getStockPriceInfo(ts_code, self.stock_picked_date)       
            if dic_stock_price is None:
                continue      
            if dic_stock_price['circ_mv']  > self.circ_mv_max or dic_stock_price['turnover_rate_f'] < turnover_rate_f_min \
                or dic_stock_price['high_250'] / dic_stock_price['low_250'] > self.pct_chg_max_year \
                    or dic_stock_price['ma_250'] > dic_stock_price['ma_120'] or dic_stock_price['ma_120'] > dic_stock_price['ma_60'] \
                        or dic_stock_price['ma_60'] > dic_stock_price['ma_20'] or dic_stock_price['ma_20'] > dic_stock_price['ma_5'] \
                            or dic_stock_price['close'] > dic_stock_price['ma_5'] * self.pct_close_to_ma5:
                continue
            lst_code_pool.append(dic_stock_price['ts_code'])
        lst_n_days = ds_tushare.get_pre_n_trade_date(self.stock_picked_date, self.n_days)   # 日期从大到小排列
        arr_code = list()
        arr_a1 = list() # 最近一天的数据
        arr_a2 = list()
        arr_a3 = list()
        arr_a4 = list()
        arr_a5 = list()
        arr_b1 = list()
        arr_b2 = list()
        arr_b3 = list()
        arr_b4 = list()
        arr_b5 = list()
        for item_code in lst_code_pool:
            lst_stock_price = ds_tushare.getStockPriceLst(ts_code, lst_n_days[-1], lst_n_days[0])   
            if len(lst_stock_price) < self.n_days:
                # 排除最近5个交易日有停牌情况的股票
                continue
            arr_code.append(item_code)
            idx = 0
            for item_price in lst_stock_price:
                idx += 1
                if idx == 1:
                    # 第一天数据 n-1
                    arr_a1.append(item_price['turnover_rate_f'])
                    arr_b1.append(item_price['volume_ratio'])
                elif idx == 2:
                    # 第二天数据 n-2
                    arr_a2.append(item_price['turnover_rate_f'])
                    arr_b2.append(item_price['volume_ratio'])
                elif idx == 3:
                    arr_a3.append(item_price['turnover_rate_f'])
                    arr_b3.append(item_price['volume_ratio'])
                elif idx == 4:
                    arr_a4.append(item_price['turnover_rate_f'])
                    arr_b4.append(item_price['volume_ratio'])
                elif idx == 5:
                    arr_a5.append(item_price['turnover_rate_f'])
                    arr_b5.append(item_price['volume_ratio'])
                else:
                    self.logger.info('lst_stock_price data error!!!')
                    self.logger.info(lst_stock_price)
                    break

"""
to do:
统计量比，换手率排名选股
计算股票池的每日涨跌幅（叠加大盘指数绘图）
"""                    