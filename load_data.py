
from test import Ui_MainWindow
from PyQt5 import QtCore, QtGui, uic,QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys,os

class LoadData(QtWidgets.QMainWindow,Ui_MainWindow):
    def __int__(self,parent=None):
        super(LoadData,self).__int__(parent)
        self.setupUi(self)
        self.load_data.clicked.connect(self.show_vis)

    def show_vis(self):
        self.DataGraph.setPixmap(QPixmap('C:\\2.jpg'))
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    window=LoadData()
    window.show()
    sys.exit(app.exec_())


