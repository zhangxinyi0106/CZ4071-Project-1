from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
from preprocessing import *
from faculty import *
import threading

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
        for i in range(5):
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
        questionList = ["Select one", "Degree distribution", "Average Degree", "Clustering coefficient", "Diameter"]
        options = ["Select one", "collaboration between faculty of different ranks",
                   "collaboration between faculty holding or held management position and non-management faculty",
                   "collaboration between faculty of different areas in computer science",
                   "are central nodes of the network measured using network properties identical to excellence nodes"]
        for i in range(2001, 2022):
            selectYearText.append("show network until year "+str(i))
        for i in range(23):
            self.comboBox.setItemText(i, _translate("Interface", selectYearText[i]))
        for i in range(5):
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
        port = get_free_port()
        t = threading.Thread(target=self.callApi, args=(ret,port), name='function')
        t.start()
        QDesktopServices.openUrl(QUrl('http://127.0.0.1:' + str(port) + '/'))
        return ret
    def callApi(self,ret,p):
        analyzer = Analyzer()
        T, G = generate_graphs(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles)
        subgraphs = analyzer.filter_graph_by_names(G, ret)
        visualize_graphs(tags=T, graphs=subgraphs, port=p)

class propertyDialog(object):
    def setupUi(self, Form, i):
        Form.setObjectName("Form")
        Form.resize(904, 648)
        self.summary = QtWidgets.QLabel(Form)
        self.summary.setGeometry(QtCore.QRect(50, 50, 101, 31))
        self.summary.setObjectName("summary")
        self.graph = QtWidgets.QLabel(Form)
        self.graph.setGeometry(QtCore.QRect(470, 50, 91, 41))
        self.graph.setObjectName("graph")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 90, 411, 461))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(700, 560, 116, 30))
        #self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        #self.horizontalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(Form.myWindow)
        self.buttonBox.rejected.connect(Form.myWindow)
        self.retranslateUi(Form, i)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form, i):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setGeometry(QtCore.QRect(460, 90, 401, 461))
        self.label_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_2.setText("")
        analyzer = Analyzer()
        if i == 1:
            G = generate_graph(name_data=analyzer.auth_name_data,
                               profile_data=analyzer.auth_profiles,
                               by_year=2020)
            self.summary.setText(_translate("Form", "degree distribution histogram"))
            self.summary.setGeometry(QtCore.QRect(50, 50, 401, 31))
            self.graph.setText(_translate("Form", "degree distribution loglog"))
            self.graph.setGeometry(QtCore.QRect(470, 50, 401, 41))
            self.label.setScaledContents(True)
            self.label_2.setScaledContents(True)
            self.label.setPixmap(QtGui.QPixmap("pictures/"
                                               + analyzer.plot_degree_distribution_hist(G)))
            self.label_2.setPixmap(QtGui.QPixmap("pictures/"
                                                 + analyzer.plot_degree_distribution_loglog(G,
                                                                                            normalized=False)))

        else:
            Tag, Graphs = generate_graphs(name_data=analyzer.auth_name_data,
                                          profile_data=analyzer.auth_profiles)
            if i==2:
                text = ""
                for i in range(2000, 2021):
                    t = "Average degree for year " + str(i) + ": "\
                        + str("{:.7f}".format(analyzer.get_avg_degree(Graphs[i-2000]))) + "\n"
                    text += t
                self.label.setText(text)
                self.label_2.setPixmap(QtGui.QPixmap("pictures/"
                                                     + analyzer.plot_avg_degree_hist(Graphs, Tag)))
            elif i==3:
                text = ""
                for i in range(2000, 2021):
                    t = "Clustering coefficient for year " + str(i) + ": " \
                        + str("{:.7f}".format(analyzer.get_clustering_coeff(Graphs[i-2000]))) + "\n"
                    text += t
                self.label.setText(text)
                self.label_2.setPixmap(QtGui.QPixmap("pictures/"
                                                     + analyzer.plot_avg_clust_coeff_hist(Graphs, Tag)))
            elif i==4:
                text = ""
                for i in range(2000, 2021):
                    t = "Diameter for year " + str(i) + ": " \
                        + str(analyzer.get_largest_component_diameter(Graphs[i-2000])) + "\n"
                    text += t
                self.label.setText(text)
                self.label_2.setPixmap(QtGui.QPixmap("pictures/"
                                                     + analyzer.plot_diameter_hist(Graphs, Tag)))
            else:
                self.label.setText(_translate("Form", "Nothing"))
                self.label_2.setPixmap(QtGui.QPixmap("pictures/no_image_available.png"))
            self.label_2.setScaledContents(True)
            self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
            self.label_2.setObjectName("label_2")
            self.summary.setText(_translate("Form", "Summary"))
            self.graph.setText(_translate("Form", "Graph"))

class analyzeDialog(object):
    def setupUi(self, Form, i):
        Form.setObjectName("Form")
        Form.resize(1014, 815)
        self.summary = QtWidgets.QLabel(Form)
        self.summary.setGeometry(QtCore.QRect(30, 46, 177, 23))
        self.summary.setObjectName("summary")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 760, 671, 25))
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
        self.label_2.setGeometry(QtCore.QRect(20, 80, 301, 300))
        self.label_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.label_2.setIndent(2)
        self.label_2.setScaledContents(True)
        self.label_2.setPixmap(QtGui.QPixmap("pictures/insts_collab.png"))

        self.retranslateUi(Form, i)
        self.ok.clicked.connect(Form.myWindow)
        self.cancel.clicked.connect(Form.myWindow)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form, i):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.analyzer = Analyzer()
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
            self.tableView.setGeometry(QtCore.QRect(370, 80, 601, 621))
            self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
            self.tableView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
            self.tableView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
            self.tableView.setObjectName("tableView")
            self.summary.setText(_translate("Form", "Degree increase graph"))
            self.label.setText(_translate("Form", "Table"))
            self.tableView.setColumnCount(21)
            self.tableView.setRowCount(10)
            self.tableView.setHorizontalHeaderLabels([str(num) for num in range(2000, 2021)])
            self.tableView.setVerticalHeaderLabels(
                ["number of partners",               "total number of collab papers",
                 "total number of published venues", "relative number of partners",
                 "relative number of collab papers", "relative number of published venues",
                 "betweenness centrality",           "closeness_centrality",
                 "eigenvector_centrality",           "most frequent venues"]
            )
            self.submitClicked = False
            selectYearText = ["Select one graph", "show graph 2000 ~ 2001"]
            for n in range(2001, 2020):
                selectYearText.append("show graph " + str(n) + " ~ " + str(n + 1))
            self.comboBox = QtWidgets.QComboBox(Form)
            self.comboBox.setGeometry(QtCore.QRect(20, 400, 311, 30))
            self.comboBox.setObjectName("comboBox")
            for j in range(21):
                self.comboBox.addItem("")
            for k in range(21):
                self.comboBox.setItemText(k, selectYearText[k])
            self.comboBox.currentIndexChanged.connect(self.updateGraph)
            self.submit = QtWidgets.QPushButton(Form)
            self.submit.setObjectName("submit")
            self.submit.setText(_translate("Form", "submit"))
            self.submit.setGeometry(QtCore.QRect(20, 700, 300, 30))
            self.submit.clicked.connect(self.checkstatus)

            if i==2:
                self.checkbox1 = QtWidgets.QCheckBox(Form)
                self.checkbox1.setGeometry(QtCore.QRect(80, 450, 120, 30))
                self.checkbox1.setObjectName("rank1")
                self.checkbox1.setText(_translate("Dialog", "Management-only"))
                self.option = 2
            else:
                self.names = self.analyzer.auth_name_data['Position'].unique() if i == 1 \
                    else self.analyzer.auth_name_data['Area'].unique()
                self.option = 1 if i == 1 \
                    else 3
                self.scrollArea = QtWidgets.QScrollArea(Form)
                self.scrollArea.setGeometry(QtCore.QRect(20, 450, 300, 236))
                self.scrollArea.setFrameShape(QtWidgets.QFrame.Panel)
                self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
                self.scrollArea.setWidgetResizable(True)
                self.scrollArea.setObjectName("scrollArea")
                self.scrollAreaWidgetContents = QtWidgets.QWidget()
                self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 270, 300))
                self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
                self.formLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
                self.formLayout.setObjectName("formLayout")
                self.numOfCheckbox = len(self.names)
                self.checkboxes = []
                for n in range(self.numOfCheckbox):
                    checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
                    checkBox.setObjectName("checkBox" + str(n))
                    self.formLayout.setWidget(n, QtWidgets.QFormLayout.LabelRole, checkBox)
                    self.checkboxes.append(checkBox)
                self.scrollArea.setWidget(self.scrollAreaWidgetContents)
                for n in range(self.numOfCheckbox):
                    self.checkboxes[n].setText(self.names[n])

        self.ok.setText(_translate("Form", "OK"))
        self.cancel.setText(_translate("Form", "Cancel"))

    def checkstatus(self):
        self.submitClicked = True
        ret = []
        if self.option != 2:
            for i in range(self.numOfCheckbox):
                exec("""if self.checkboxes[i].isChecked():
                        ret.append(self.checkboxes[i].text())""".format(i, i))
            print(ret)
        else:
            if self.checkbox1.isChecked():
                ret.append(True)
            else:
                ret.append(False)

        i = self.option
        port = get_free_port()
        t = threading.Thread(target=self.callApi, args=(i,ret,port,), name='function')
        t.start()
        QDesktopServices.openUrl(QUrl('http://127.0.0.1:' + str(port) + '/'))

    def callApi(self, i, ret, p):
        print("if the port refused to connect, please wait for the server to be ready and reload.")
        T, G = generate_graphs(name_data=self.analyzer.auth_name_data, profile_data=self.analyzer.auth_profiles)

        no_comp = []
        if i == 1:
            self.subgraphs = self.analyzer.filter_graph_by_rank(G, ret)
        elif i==2:
            self.subgraphs = self.analyzer.filter_graph_by_managerole(G, ret[0])
        else:
            self.subgraphs = self.analyzer.filter_graph_by_area(G, ret)
        delta_k_data = self.analyzer.get_degree_increase(self.subgraphs)
        self.degree_inc_pic_names = []
        for j in range(0, len(delta_k_data)):
            if delta_k_data[j]:
                self.degree_inc_pic_names.append(self.analyzer.visualize_degree_increase(delta_k_data[j]))
            else:
                self.degree_inc_pic_names.append("no_image_available.jpg")
        total_num_of_partners, total_num_of_papers, \
        total_num_of_venues, most_frequent_venues \
            = self.analyzer.get_colab_properties(graphs=self.subgraphs)
        relative_weight = self.analyzer.get_relative_colab_weight(self.subgraphs, G)
        centrality = []
        for i in range(21):
            try:
                centrality.append(self.analyzer.analyze_centrality_of_main_component(self.subgraphs[i]))
                no_comp.append(False)
            except ValueError:
                no_comp.append(True)
        for n in range(21):
            self.tableView.setItem(0, n, QTableWidgetItem(str(total_num_of_partners[n])))
            self.tableView.setItem(1, n, QTableWidgetItem(str(total_num_of_papers[n])))
            self.tableView.setItem(2, n, QTableWidgetItem(str(total_num_of_venues[n])))
            self.tableView.setItem(3, n, QTableWidgetItem(str("{:.5f}".format(relative_weight[0][n]))))
            self.tableView.setItem(4, n, QTableWidgetItem(str("{:.5f}".format(relative_weight[1][n]))))
            self.tableView.setItem(5, n, QTableWidgetItem(str("{:.5f}".format(relative_weight[2][n]))))
            if not no_comp[n]:
                self.tableView.setItem(6, n, QTableWidgetItem(str(centrality[0]["betweenness_centrality"])))
                self.tableView.setItem(7, n, QTableWidgetItem(str(centrality[1]["closeness_centrality"])))
                self.tableView.setItem(8, n, QTableWidgetItem(str(centrality[2]["eigenvector_centrality"])))
            self.tableView.setItem(9, n, QTableWidgetItem(str(most_frequent_venues[n])))
        visualize_graphs(tags=T, graphs=self.subgraphs, port=p)

    def updateGraph(self, i):
        if self.submitClicked:
            self.label_2.setScaledContents(True)
            self.label_2.setPixmap(QtGui.QPixmap("pictures/" + self.degree_inc_pic_names[i-1]))

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
        self.property.setGeometry(QtCore.QRect(10, 40, 271, 42))
        self.property.setObjectName("property")
        self.property.addItem("")
        self.property.addItem("")
        #self.property.addItem("")
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
        self.property.setItemText(0, _translate("Form", "the growth and speed of growth"))
        self.property.setItemText(1, _translate("Form", "number of top papers"))
        #self.property.setItemText(2, _translate("Form", "Property3"))

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