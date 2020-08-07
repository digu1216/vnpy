from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys
import numpy as np
from PyQt5.QtWidgets import QGridLayout

from ui.Ui_stock_pool_track import Ui_MainWindow


#创建一个matplotlib图形绘制类
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
        self.plotcos()
    
    #第四步：就是画图，【可以在此类中画，也可以在其它类中画】
    def plotcos(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes.plot(t, s)
    
    def plot_yield_curve(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes.plot(t, s)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建QWidget窗体
        self.__ui = Ui_MainWindow()  # 创建UI对象
        self.__ui.setupUi(self)  # 构造UI     
        self.__ui.dateEdit.setDate(QtCore.QDate.fromString('20200806', 'yyyyMMdd'))
        # self.__ui.dateEdit_2.dateChanged[QtCore.QDate].connect(self.slot_test)

        #第五步：定义MyFigure类的一个实例
        self.F = MyFigure(width=3, height=2, dpi=100)        
        # self.plotcos()
        #第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        # self.gridlayout = QGridLayout(self.groupBox)  # 继承容器groupBox
        # self.gridlayout.addWidget(self.F,0,1)
        self.__ui.verticalLayout.addWidget(self.F)
        
        # self.fig = Figure(figsize=(8, 10), dpi=100)              
        # self.fig = Figure()              
        # self.canvas = FigureCanvas(self.fig)
        # self.axes = self.fig.add_subplot(111)   
        # t = np.arange(0.0, 3.0, 0.01)
        # s = np.sin(2 * np.pi * t)
        # self.axes.plot(t, s)
        # # self.gridlayout = QGridLayout(self.__ui.widget)
        # # self.__ui.gridlayout.addWidget(self.canvas, 0, 0)
        # self.__ui.verticalLayout.addWidget(self.canvas)
    def slot_test(self, date):
        # self.__ui.textEdit.setText('AAAAAAAAAAAAAAAAAAAA')
        self.__ui.textEdit.setText(date.toString("yyyyMMdd"))

    def on_dateEdit_2_dateChanged(self, date):
        self.__ui.textEdit.setText(date.toString("yyyyMMdd"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建app，用QApplication类
    myWidget = MainWindow()
    myWidget.show()    
    sys.exit(app.exec_())
    