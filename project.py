import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import threading

from interface import Ui_MainWindow, Ui_Dialog, checkbox_Dialog, \
    newFacultyDialog, propertyDialog, analyzeDialog, facultyMemDialog
from faculty import Analyzer
from preprocessing import *


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def myWindow(self):
        self.hide()
        self.myWin = MyWindow()
        self.myWin.show()


class newFalDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = newFacultyDialog()
        self.ui.setupUi(self)

    def myWindow(self):
        self.hide()
        self.myWin = MyWindow()
        self.myWin.show()


class FalMemDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = facultyMemDialog()
        self.ui.setupUi(self)

    def myWindow(self):
        self.hide()
        self.myWin = MyWindow()
        self.myWin.show()

    def setFacultyList(self, facultyList):
        self.ui.facultyList = facultyList


class propertyDia(QDialog):
    def __init__(self, i):
        super().__init__()
        self.ui = propertyDialog()
        self.ui.setupUi(self, i)

    def myWindow(self):
        self.hide()
        self.myWin = MyWindow()
        self.myWin.show()


class AnalyzeDia(QDialog):
    def __init__(self, i):
        super().__init__()
        self.ui = analyzeDialog()
        self.ui.setupUi(self, i)

    def myWindow(self):
        self.hide()
        self.myWin = MyWindow()
        self.myWin.show()


class CheckBox(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = checkbox_Dialog()
        self.ui.setupUi(self)

    def myWindow(self):
        self.hide()
        self.myWin = MyWindow()
        self.myWin.show()

    def falcultyMem(self):
        self.hide()
        self.new = FalMemDialog()
        self.new.show()
        self.new.setFacultyList(self.ui.getFacultyList())

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        gridLayout = QGridLayout(centralWidget)
        gridLayout.addWidget(self.ui.label, 1, 0, alignment=Qt.AlignCenter)
        gridLayout.addWidget(self.ui.label_2, 0, 0, alignment=Qt.AlignCenter)
        gridLayout.addWidget(self.ui.pushButton, 6, 0)
        gridLayout.addWidget(self.ui.pushButton2, 5, 0)
        gridLayout.addWidget(self.ui.comboBox, 2, 0)
        gridLayout.addWidget(self.ui.comboBox2, 3, 0)
        gridLayout.addWidget(self.ui.comboBox3, 4, 0)

    def dialogbox(self):
        self.hide()
        self.myDialog = MyDialog()
        self.myDialog.show()

    def newFacultyD(self):
        self.hide()
        self.myDialog2 = newFalDialog()
        self.myDialog2.show()
        port = get_free_port()
        t = threading.Thread(target=self.newFacApi, args=(port,), name='function')
        t.start()
        QDesktopServices.openUrl(QUrl('http://127.0.0.1:' + str(port) + '/'))

    def newFacApi(self, p):
        analyzer = Analyzer()
        analyzer.use_external_collaborators_profiles()
        sorted_namelist, external_profiles = analyzer.get_new_member_profile(based_on_excellece=True)
        G_new = generate_graph(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles,
                               external_profile_data=external_profiles)
        visualize_graph(graph=G_new, port=p)

    def facultyMemD(self):
        self.hide()
        self.myDialog2 = FalMemDialog()
        self.myDialog2.show()

    def propertyD(self, i):
        if i == 0:
            pass
        else:
            self.hide()
            self.myDialog3 = propertyDia(i)
            self.myDialog3.show()

    def analyzeD(self, i):
        if i == 0:
            pass
        else:
            self.hide()
            self.myDialog4 = AnalyzeDia(i)
            self.myDialog4.show()

    def checkbox(self):
        self.hide()
        self.cb = CheckBox()
        self.cb.show()

    def update(self,year,p):
        analyzer = Analyzer()
        G = generate_graph(analyzer.auth_name_data, analyzer.auth_profiles, by_year=year)
        visualize_graph(graph=G,port=p)

    def updateGraph(self, i):
        if i == 0:
            pass
        else:
            year = 2000 + i - 1
            print("chose year: ", year)
            port=get_free_port()
            t = threading.Thread(target=self.update, args=(year,port,), name='function')
            t.start()
            QDesktopServices.openUrl(QUrl('http://127.0.0.1:'+str(port)+'/'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
