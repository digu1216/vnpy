import numpy as np
import pymongo
from logger import Logger
from data_service import DataServiceTushare

if __name__ == "__main__":
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    stock = db['stock_digu']
    col_index_data = stock['000001.SH']
    logger = Logger().getlog()
    ds_tushare = DataServiceTushare()
    lst_trade_date = ds_tushare.getTradeCal('19891201')
    vol_lst = list()
    for item_date in lst_trade_date:
        if len(vol_lst) != 5:
            data = col_index_data.find_one({"trade_date": item_date})            
            data['qrr'] = 0
            col_index_data.update_one({"trade_date": item_date}, {"$set": data})
            vol_lst.append(data['vol'])
        else:                                 
            data = col_index_data.find_one({"trade_date": item_date})            
            data['qrr'] = data['vol']/(sum(vol_lst)/5)            
            col_index_data.update_one({"trade_date": item_date}, {"$set": data})
            vol_lst.append(data['vol'])
            vol_lst.pop(0)
