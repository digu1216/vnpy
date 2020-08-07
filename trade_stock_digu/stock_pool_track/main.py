from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys
import numpy as np
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout

from ui.Ui_stock_pool_track import Ui_MainWindow
from datetime import datetime
from datetime import timedelta
from vnpy.tools.convert_utils import string_to_datetime, time_to_str
from vnpy.tools.logger import Logger
from vnpy.trade_stock_digu.data_service import DataServiceTushare, LOG

#创建一个matplotlib图形绘制类
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
    
    #第四步：就是画图，【可以在此类中画，也可以在其它类中画】
    def plotcos(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes.plot(t, s)
    
    def plot_yield_curve(self, x, y):
        t = np.array(x)
        s = np.array(y)
        self.axes.plot(t, s)

class MainWindow(QtWidgets.QMainWindow):
    ds_tushare = DataServiceTushare()
    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建QWidget窗体
        self.__ui = Ui_MainWindow()  # 创建UI对象
        self.__ui.setupUi(self)  # 构造UI   
        self.__ui.dateEdit.setDate(QtCore.QDate.fromString(time_to_str(datetime.now(), '%Y%m%d'), 'yyyyMMdd'))
        self.__ui.dateEdit_3.setDate(QtCore.QDate.fromString(time_to_str(datetime.now(), '%Y%m%d'), 'yyyyMMdd'))
        self.draw_cur_yield_curve()
        self.draw_history_yield_curve()
        # self.__ui.dateEdit_2.dateChanged[QtCore.QDate].connect(self.slot_test)  # 显示connect的方法

    # def slot_test(self, date):
    #     # self.__ui.textEdit.setText('AAAAAAAAAAAAAAAAAAAA')
    #     self.__ui.textEdit.setText(date.toString("yyyyMMdd"))

    def draw_cur_yield_curve(self):
        #第五步：定义MyFigure类的一个实例
        self.F_cur = MyFigure(width=3, height=2, dpi=100)
        self.F_cur.plot_yield_curve(1, 2)
        #第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.gridlayout_cur = QGridLayout(self.__ui.groupBox)  # 继承容器groupBox
        self.gridlayout_cur.addWidget(self.F_cur,0,0)

    def draw_history_yield_curve(self, date=None):
        #第五步：定义MyFigure类的一个实例
        self.F_his = MyFigure(width=3, height=2, dpi=100)
        self.F_his.plot_yield_curve(1, 2)
        #第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.gridlayout_his = QGridLayout(self.__ui.groupBox_2)  # 继承容器groupBox
        self.gridlayout_his.addWidget(self.F_his,0,1)

    def on_dateEdit_2_dateChanged(self, date):
        self.__ui.textEdit.setText(date.toString("yyyyMMdd"))

    @pyqtSlot() #对槽函数参数加上pyqtSlot后，不带参数的槽函数只会接收不带参数的槽函数信号，则槽函数只会触发一次。
    def on_pushButton_clicked(self):
        content = self.__ui.textEdit.toPlainText()
        content_sell = self.__ui.textEdit_2.toPlainText()
        date = self.__ui.dateEdit_3.date()
        lst_code = content.split(',')
        lst_code_sell = content_sell.split(',')
        lst_code_transfer = list()
        lst_code_transfer_sell = list()
        code_error = False
        if content == '':
            lst_code = []
        if content_sell == '':
            lst_code_sell = []
        for item in lst_code:
            if item[0] in ['0', '3']:
                item += '_SZ'
            else:
                item += '_SH'
            if item not in self.ds_tushare.get_stock_list():
                LOG.info('stock code error! %s' %item)
                code_error = True
                break
            lst_code_transfer.append(item)
        for item in lst_code_sell:
            if item[0] in ['0', '3']:
                item += '_SZ'
            else:
                item += '_SH'
            if item not in self.ds_tushare.get_stock_list():
                LOG.info('stock code error! %s' %item)
                code_error = True
                break
            lst_code_transfer_sell.append(item)
        if code_error is False:
            self.ds_tushare.daily_stock_pool_in_db(lst_code_transfer, date.toString("yyyyMMdd"))
            self.ds_tushare.cur_stock_pool_in_db(lst_code_transfer, date.toString("yyyyMMdd"))
            self.ds_tushare.set_daily_stock_pool(lst_code_transfer_sell, date.toString("yyyyMMdd"))
            self.ds_tushare.del_cur_stock_pool(lst_code_transfer_sell, date.toString("yyyyMMdd"))
            self.__ui.textEdit.clear()
            self.__ui.textEdit_2.clear()

    def count_cur_yield_by_date(self):
        date_lst = self.ds_tushare.get_cur_stock_pool_date_lst()
        rate_lst = list()
        idx = 0
        code_lst_pre = list()
        for item in date_lst:
            if idx == 0
                rate_lst.append(1.0)
                code_lst_pre = self.ds_tushare.get_cur_stock_pool(item)
            else:

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建app，用QApplication类
    myWidget = MainWindow()
    myWidget.show()    
    sys.exit(app.exec_())
    