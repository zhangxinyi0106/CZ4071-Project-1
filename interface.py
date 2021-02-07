from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Interface(object):
    def setupUi(self, Interface):
        Interface.setObjectName("Interface")
        Interface.resize(900, 800)
        self.centralwidget = QtWidgets.QWidget(Interface)
        self.centralwidget.setObjectName("centralwidget")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(280, 410, 200, 50))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pictures/blue-arrow-button-png.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commandLinkButton.setIcon(icon)
        self.commandLinkButton.setIconSize(QtCore.QSize(40, 40))
        self.commandLinkButton.setShortcut("")
        self.commandLinkButton.setCheckable(False)
        self.commandLinkButton.setChecked(False)
        self.commandLinkButton.setAutoRepeat(False)
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 260, 800, 150))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 850, 150))
        self.label_2.setObjectName("label_2")
        Interface.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Interface)
        self.statusbar.setObjectName("statusbar")
        Interface.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(Interface)
        self.toolBar.setObjectName("toolBar")
        Interface.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(Interface)
        QtCore.QMetaObject.connectSlotsByName(Interface)

    def retranslateUi(self, Interface):
        _translate = QtCore.QCoreApplication.translate
        Interface.setWindowTitle(_translate("Interface", "Interface"))
        self.commandLinkButton.setText(_translate("Interface", "Show graph"))
        self.label.setText(_translate("Interface",
                                      "<html><head/><body><p align=\"center\"><span style=\" "
                                      "font-weight:600; color:#ff0000;\">"
                                      "Welcome to NTU SCSE network analysis system</span>"
                                      "</p><p align=\"center\">Brought to you by Group : "
                                      "<span style=\" font-style:italic;\">Xia Chenguang, Zhang Xinyi,"
                                      " Zhou Hongyu, Hu Wenqi</span></p></body></html>"))
        self.label_2.setText(_translate("Interface", "<html><head/><body><p align=\"center\">"
                                                     "<img src=\"pictures/network_3_720x160.jpg\"/>"
                                                     "</p></body></html>"))
        self.toolBar.setWindowTitle(_translate("Interface", "toolBar"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Interface = QtWidgets.QMainWindow()
    ui = Ui_Interface()
    ui.setupUi(Interface)
    Interface.show()
    sys.exit(app.exec_())
