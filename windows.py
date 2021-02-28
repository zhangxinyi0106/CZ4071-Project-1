from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 260, 800, 150))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 300, 200, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 300, 200, 27))
        self.pushButton.setObjectName("pushButton2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 850, 150))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 290, 611, 51))
        self.comboBox.setObjectName("comboBox")
        for i in range(23):
            self.comboBox.addItem("")
        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox2.setGeometry(QtCore.QRect(50, 290, 611, 51))
        self.comboBox2.setObjectName("comboBox2")
        for i in range(4):
            self.comboBox2.addItem("")
        self.comboBox3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox3.setGeometry(QtCore.QRect(50, 290, 611, 51))
        self.comboBox3.setObjectName("comboBox3")
        for i in range(5):
            self.comboBox3.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 685, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.checkbox)
        self.pushButton2.clicked.connect(MainWindow.newFacultyD)
        self.comboBox.currentIndexChanged.connect(MainWindow.updateGraph)
        self.comboBox2.currentIndexChanged.connect(MainWindow.propertyD)
        self.comboBox3.currentIndexChanged.connect(MainWindow.analyzeD)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" "
                                      "font-weight:600; color:#ff0000;\">"
                                      "Welcome to NTU SCSE network analysis system</span>"
                                      "</p><p align=\"center\">Brought to you by Group : "
                                      "<span style=\" font-style:italic;\">Xia Chenguang, Zhang Xinyi,"
                                      " Zhou Hongyu, Hu Wenqi</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">"
                                                     "<img src=\"pictures/network_3_720x160.jpg\"/>"
                                                     "</p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Select faculty members"))
        self.pushButton2.setText(_translate("MainWindow", "Add new faculty"))
        selectYearText = ["Select one", "show network until year 2000"]
        questionList = ["Select one", "p1", "p2", "p3"]
        options = ["Select one", "collaboration between faculty of different ranks",
                   "collaboration between faculty holding or held management position and non-management faculty",
                   "collaboration between faculty of different areas in computer science",
                   "are central nodes of the network measured using network properties identical to excellence nodes"]
        for i in range(2001, 2022):
            selectYearText.append("show network until year "+str(i))
        for i in range(23):
            self.comboBox.setItemText(i, _translate("Interface", selectYearText[i]))
        for i in range(4):
            self.comboBox2.setItemText(i, _translate("Interface", questionList[i]))
        for i in range(5):
            self.comboBox3.setItemText(i, _translate("Interface", options[i]))
        #file = pd.read_excel("data/Faculty.xlsx")
        #facultyList = file["Faculty"]


class Ui_Dialog(object):
    def setupUi(self, Dialog2):
        Dialog2.setObjectName("Dialog2")
        Dialog2.resize(835, 549)
        self.label_2 = QtWidgets.QLabel(Dialog2)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 751, 401))
        self.label_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("pictures/graph2.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog2)
        self.label_3.setGeometry(QtCore.QRect(31, 35, 311, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog2)
        self.label_4.setGeometry(QtCore.QRect(110, 20, 641, 31))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.widget = QtWidgets.QWidget(Dialog2)
        self.widget.setGeometry(QtCore.QRect(30, 480, 751, 61))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setMinimum(2000)
        self.spinBox.setMaximum(2021)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog2)
        self.buttonBox.accepted.connect(Dialog2.myWindow)
        self.buttonBox.rejected.connect(Dialog2.myWindow)
        self.pushButton.clicked.connect(self.label_2.update)
        QtCore.QMetaObject.connectSlotsByName(Dialog2)

    def retranslateUi(self, Dialog2):
        _translate = QtCore.QCoreApplication.translate
        Dialog2.setWindowTitle(_translate("Dialog2", "Dialog"))
        self.label_3.setText(_translate("Dialog2", "Graph"))
        self.label_4.setText(_translate("Dialog2", "Evolvement of network since year 2000"))
        self.label.setText(_translate("Dialog2", "select year"))
        self.pushButton.setText(_translate("Dialog2", "Load graph"))


class checkbox_Dialog(object):

    def setupUi(self, Dialog):
        self.facultyList = pd.read_excel("data/Faculty.xlsx")["Faculty"]
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 800)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(200, 50))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 474, 348))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.scrollAreaWidgetContents)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        #self.horizontalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(Dialog.falcultyMem)
        self.buttonBox.accepted.connect(self.findState)
        self.buttonBox.rejected.connect(Dialog.myWindow)
        # self.okButton = QtWidgets.QPushButton(Dialog)
        # self.okButton.setGeometry(QtCore.QRect(230, 40, 71, 31))
        # font = QtGui.QFont()
        # font.setPointSize(14)
        # self.okButton.setFont(font)
        # self.okButton.setObjectName("okButton")
        # self.okButton.clicked.connect(self.findState)
        # self.okButton.clicked.connect(Dialog.myWindow)
        for i in range(1,18):
            exec("""self.horizontalLayout_{} = QtWidgets.QHBoxLayout()
self.horizontalLayout_{}.setObjectName("horizontalLayout_{}")
self.checkbox_{} = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
self.checkbox_{}.setObjectName("{}")
self.horizontalLayout_{}.addWidget(self.checkbox_{})
self.checkbox_{} = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
self.checkbox_{}.setObjectName("{}")
self.horizontalLayout_{}.addWidget(self.checkbox_{})
self.checkbox_{} = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
self.checkbox_{}.setObjectName("{}")
self.horizontalLayout_{}.addWidget(self.checkbox_{})
self.checkbox_{} = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
self.checkbox_{}.setObjectName("{}")
self.horizontalLayout_{}.addWidget(self.checkbox_{})
self.checkbox_{} = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
self.checkbox_{}.setObjectName("{}")
self.horizontalLayout_{}.addWidget(self.checkbox_{})
self.gridLayout.addLayout(self.horizontalLayout_{}, {}, 0, 1, 1)
            """.format(i,i,i,(i-1)*5,(i-1)*5,self.facultyList[(i-1)*5],i,(i-1)*5,
                       (i-1)*5+1,(i-1)*5+1,self.facultyList[(i-1)*5+1],i,(i-1)*5+1,
                       (i-1)*5+2,(i-1)*5+2,self.facultyList[(i-1)*5+2],i,(i-1)*5+2,
                       (i-1)*5+3,(i-1)*5+3,self.facultyList[(i-1)*5+3],i,(i-1)*5+3,
                       (i - 1) * 5+4, (i - 1) * 5+4, self.facultyList[(i - 1) * 5+4], i, (i - 1) * 5+4,
                       i, i-1))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.buttonBox)
        #self.verticalLayout.addWidget(self.okButton)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        #self.okButton.setText(_translate("Dialog", "ok"))
        for i in range(85):
            exec("""self.checkbox_{}.setText(_translate("Dialog", "{}"))""".format(i,self.facultyList[i]))

    def findState(self):
        ret = []
        for i in range(85):
            exec("""if self.checkbox_{}.isChecked():
    ret.append(self.checkbox_{}.text())""".format(i, i))
        print(ret)
        QDesktopServices.openUrl(QUrl('http://127.0.0.1:8080/'))
        return ret

class propertyDialog(object):
    def setupUi(self, Form, i):
        Form.setObjectName("Form")
        Form.resize(704, 548)
        self.summary = QtWidgets.QLabel(Form)
        self.summary.setGeometry(QtCore.QRect(50, 50, 101, 31))
        self.summary.setObjectName("summary")
        self.graph = QtWidgets.QLabel(Form)
        self.graph.setGeometry(QtCore.QRect(370, 50, 91, 41))
        self.graph.setObjectName("graph")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(120, 480, 431, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 90, 311, 361))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(Form.myWindow)
        self.buttonBox.rejected.connect(Form.myWindow)
        self.retranslateUi(Form, i)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form, i):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setGeometry(QtCore.QRect(360, 90, 301, 361))
        self.label_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_2.setText("")
        if i==1:
            self.label.setText(_translate("Form", "TextLabel1"))
            self.label_2.setPixmap(QtGui.QPixmap("pictures/graph.png"))
        elif i==2:
            self.label.setText(_translate("Form", "TextLabel2"))
            self.label_2.setPixmap(QtGui.QPixmap("pictures/graph2.png"))
        else:
            self.label.setText(_translate("Form", "TextLabel3"))
            self.label_2.setPixmap(QtGui.QPixmap("pictures/graph3.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_2.setObjectName("label_2")
        self.summary.setText(_translate("Form", "Summary"))
        self.graph.setText(_translate("Form", "graph"))

class analyzeDialog(object):
    def setupUi(self, Form, i):
        Form.setObjectName("Form")
        Form.resize(814, 615)
        self.summary = QtWidgets.QLabel(Form)
        self.summary.setGeometry(QtCore.QRect(30, 50, 47, 13))
        self.summary.setObjectName("summary")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 560, 671, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ok.sizePolicy().hasHeightForWidth())
        self.ok.setSizePolicy(sizePolicy)
        self.ok.setObjectName("ok")
        self.horizontalLayout.addWidget(self.ok)
        self.cancel = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel.sizePolicy().hasHeightForWidth())
        self.cancel.setSizePolicy(sizePolicy)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.label = QtWidgets.QLabel(Form)

        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 301, 421))
        self.label_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form, i)
        self.ok.clicked.connect(Form.myWindow)
        self.cancel.clicked.connect(Form.myWindow)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form, i):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        if i==4:
            self.graphView = QtWidgets.QLabel(Form)

            self.summary.setText(_translate("Form", "Description"))
            self.label_2.setText(_translate("Form", "Description"))
            self.label.setGeometry(QtCore.QRect(370, 80, 351, 421))
            self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.label.setText("")
            self.label.setPixmap(QtGui.QPixmap("pictures/graph.png"))
            self.label.setScaledContents(True)
            self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        else:
            self.label.setGeometry(QtCore.QRect(380, 50, 47, 13))
            self.tableView = QtWidgets.QTableWidget(Form)
            self.tableView.setGeometry(QtCore.QRect(370, 80, 351, 421))
            self.tableView.setObjectName("tableView")
            self.summary.setText(_translate("Form", "summary"))
            self.label.setText(_translate("Form", "Table"))
            if i==1:
                self.tableView.setColumnCount(4)
                self.tableView.setRowCount(4)
                for i in range(4):
                    for j in range(4):
                        self.tableView.setItem(i, j, QTableWidgetItem("string"))
            elif i==2:
                pass
            else:
                pass
        self.ok.setText(_translate("Form", "OK"))
        self.cancel.setText(_translate("Form", "Cancel"))

        #self.label_2.setText(_translate("Form", "TextLabel"))

class facultyMemDialog(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(847, 583)
        self.graph = QtWidgets.QLabel(Form)
        self.graph.setGeometry(QtCore.QRect(300, 30, 81, 21))
        self.graph.setObjectName("graph")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(290, 100, 471, 351))
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pictures/Property1.jpg"))
        self.label.setScaledContents(True)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label_2")
        self.property = QtWidgets.QComboBox(Form)
        self.property.setGeometry(QtCore.QRect(40, 240, 121, 22))
        self.property.setObjectName("property")
        self.property.addItem("")
        self.property.addItem("")
        self.property.addItem("")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 520, 571, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(Form.myWindow)
        self.buttonBox.rejected.connect(Form.myWindow)
        self.property.currentIndexChanged.connect(self.updateGraph)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.graph.setText(_translate("Form", "Graph"))
        self.property.setItemText(0, _translate("Form", "Property1"))
        self.property.setItemText(1, _translate("Form", "Property2"))
        self.property.setItemText(2, _translate("Form", "Property3"))

    def updateGraph(self):
        imagePath = "pictures"
        currentItem = str(self.property.currentText())
        currentImage = '%s/%s.jpg' % (imagePath, currentItem)
        self.label.setPixmap(QtGui.QPixmap(currentImage))

class newFacultyDialog(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(814, 642)
        self.logic_flow = QtWidgets.QLabel(Form)
        self.logic_flow.setGeometry(QtCore.QRect(90, 90, 251, 401))
        self.logic_flow.setFrameShape(QtWidgets.QFrame.Panel)
        self.logic_flow.setObjectName("logic_flow")
        self.new_faculty = QtWidgets.QTableView(Form)
        self.new_faculty.setGeometry(QtCore.QRect(415, 91, 331, 401))
        self.new_faculty.setObjectName("new_faculty")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 570, 701, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(90, 50, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(430, 50, 47, 13))
        self.label_2.setObjectName("label_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(Form.myWindow)
        self.buttonBox.rejected.connect(Form.myWindow)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.logic_flow.setText(_translate("Form", "Logic Flow"))
        self.label.setText(_translate("Form", "Logic flow"))
        self.label_2.setText(_translate("Form", "List"))