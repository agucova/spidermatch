# Form implementation generated from reading ui file '/home/agucova/repos/spidermatch/spidermatch/windows/welcome.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_InitialWindow(object):
    def setupUi(self, InitialWindow):
        InitialWindow.setObjectName("InitialWindow")
        InitialWindow.resize(664, 560)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InitialWindow.sizePolicy().hasHeightForWidth())
        InitialWindow.setSizePolicy(sizePolicy)
        InitialWindow.setMinimumSize(QtCore.QSize(664, 560))
        InitialWindow.setMaximumSize(QtCore.QSize(664, 560))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/home/agucova/repos/spidermatch/spidermatch/windows/../assets/icon_teal.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        InitialWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(InitialWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(40, -1, 40, 30)
        self.gridLayout.setObjectName("gridLayout")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("/home/agucova/repos/spidermatch/spidermatch/windows/../assets/logo.png"))
        self.logo.setScaledContents(False)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo.setObjectName("logo")
        self.gridLayout.addWidget(self.logo, 0, 0, 1, 1)
        self.instrucciones = QtWidgets.QLabel(self.centralwidget)
        self.instrucciones.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.instrucciones.setScaledContents(False)
        self.instrucciones.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.instrucciones.setWordWrap(True)
        self.instrucciones.setOpenExternalLinks(True)
        self.instrucciones.setObjectName("instrucciones")
        self.gridLayout.addWidget(self.instrucciones, 1, 0, 1, 1)
        self.textozenserp = QtWidgets.QLabel(self.centralwidget)
        self.textozenserp.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.textozenserp.setObjectName("textozenserp")
        self.gridLayout.addWidget(self.textozenserp, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.api_token_input = QtWidgets.QLineEdit(self.centralwidget)
        self.api_token_input.setObjectName("api_token_input")
        self.horizontalLayout.addWidget(self.api_token_input)
        self.api_save_button = QtWidgets.QPushButton(self.centralwidget)
        self.api_save_button.setObjectName("api_save_button")
        self.horizontalLayout.addWidget(self.api_save_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        InitialWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(InitialWindow)
        self.statusbar.setObjectName("statusbar")
        InitialWindow.setStatusBar(self.statusbar)

        self.retranslateUi(InitialWindow)
        QtCore.QMetaObject.connectSlotsByName(InitialWindow)

    def retranslateUi(self, InitialWindow):
        _translate = QtCore.QCoreApplication.translate
        InitialWindow.setWindowTitle(_translate("InitialWindow", "Bienvenide | SpiderMatch"))
        self.instrucciones.setText(_translate("InitialWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Bienvenide a SpiderMatch! </span><span style=\" font-size:11pt;\">Para utilizar esta aplicacion debes utilizar un token de la API de Zenserp. Esto permite a SpiderMatch emitir las busquedas de Google de forma eficiente. Si no lo has hecho, puedes registrarte </span><a href=\"https://zenserp.com/\"><span style=\" font-size:11pt; text-decoration: underline; color:#1de9b6;\">aqui</span></a><span style=\" font-size:11pt;\">.</span></p></body></html>"))
        self.textozenserp.setText(_translate("InitialWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Token de Zenserp</span></p></body></html>"))
        self.api_save_button.setText(_translate("InitialWindow", "Guardar"))