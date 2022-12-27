# Form implementation generated from reading ui file '/Users/agucova/Repos/spidermatch/spidermatch/windows/panel.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PanelWindow(object):
    def setupUi(self, PanelWindow):
        PanelWindow.setObjectName("PanelWindow")
        PanelWindow.resize(1500, 1000)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PanelWindow.sizePolicy().hasHeightForWidth())
        PanelWindow.setSizePolicy(sizePolicy)
        PanelWindow.setMinimumSize(QtCore.QSize(1500, 1000))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/Users/agucova/Repos/spidermatch/spidermatch/windows/../assets/icon_teal.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        PanelWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(PanelWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(1500, 800))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.config_group_box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.config_group_box.sizePolicy().hasHeightForWidth())
        self.config_group_box.setSizePolicy(sizePolicy)
        self.config_group_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.config_group_box.setObjectName("config_group_box")
        self.config_tabs = QtWidgets.QTabWidget(self.config_group_box)
        self.config_tabs.setGeometry(QtCore.QRect(20, 40, 700, 330))
        self.config_tabs.setObjectName("config_tabs")
        self.searchTab = QtWidgets.QWidget()
        self.searchTab.setObjectName("searchTab")
        self.formLayoutWidget = QtWidgets.QWidget(self.searchTab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 751, 291))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.country_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.country_input.setObjectName("country_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.country_input)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.domain_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.domain_input.setObjectName("domain_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.domain_input)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.language_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.language_input.setObjectName("language_input")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.language_input)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.limit_input = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.limit_input.setMinimum(10)
        self.limit_input.setMaximum(100)
        self.limit_input.setSingleStep(10)
        self.limit_input.setObjectName("limit_input")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.limit_input)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.granularity_input = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.granularity_input.setMinimum(1)
        self.granularity_input.setMaximum(600)
        self.granularity_input.setSingleStep(1)
        self.granularity_input.setObjectName("granularity_input")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.granularity_input)
        self.config_tabs.addTab(self.searchTab, "")
        self.start_search_button = QtWidgets.QPushButton(self.config_group_box)
        self.start_search_button.setGeometry(QtCore.QRect(20, 400, 181, 51))
        self.start_search_button.setObjectName("start_search_button")
        self.progress_bar = QtWidgets.QProgressBar(self.config_group_box)
        self.progress_bar.setGeometry(QtCore.QRect(220, 400, 571, 51))
        self.progress_bar.setObjectName("progress_bar")
        self.gridLayout.addWidget(self.config_group_box, 1, 0, 1, 1)
        self.sites_group_box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sites_group_box.sizePolicy().hasHeightForWidth())
        self.sites_group_box.setSizePolicy(sizePolicy)
        self.sites_group_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sites_group_box.setObjectName("sites_group_box")
        self.layoutWidget = QtWidgets.QWidget(self.sites_group_box)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 40, 700, 400))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.site_list_view = QtWidgets.QListWidget(self.layoutWidget)
        self.site_list_view.setObjectName("site_list_view")
        self.verticalLayout.addWidget(self.site_list_view)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.site_import_button = QtWidgets.QPushButton(self.layoutWidget)
        self.site_import_button.setObjectName("site_import_button")
        self.horizontalLayout.addWidget(self.site_import_button)
        self.site_export_button = QtWidgets.QPushButton(self.layoutWidget)
        self.site_export_button.setObjectName("site_export_button")
        self.horizontalLayout.addWidget(self.site_export_button)
        self.site_add_button = QtWidgets.QPushButton(self.layoutWidget)
        self.site_add_button.setObjectName("site_add_button")
        self.horizontalLayout.addWidget(self.site_add_button)
        self.site_delete_button = QtWidgets.QPushButton(self.layoutWidget)
        self.site_delete_button.setObjectName("site_delete_button")
        self.horizontalLayout.addWidget(self.site_delete_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.sites_group_box, 0, 0, 1, 1)
        self.rules_group_box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rules_group_box.sizePolicy().hasHeightForWidth())
        self.rules_group_box.setSizePolicy(sizePolicy)
        self.rules_group_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rules_group_box.setObjectName("rules_group_box")
        self.layoutWidget1 = QtWidgets.QWidget(self.rules_group_box)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 40, 700, 400))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rule_list_view = QtWidgets.QListWidget(self.layoutWidget1)
        self.rule_list_view.setObjectName("rule_list_view")
        self.verticalLayout_2.addWidget(self.rule_list_view)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rule_import_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.rule_import_button.setObjectName("rule_import_button")
        self.horizontalLayout_2.addWidget(self.rule_import_button)
        self.rule_export_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.rule_export_button.setObjectName("rule_export_button")
        self.horizontalLayout_2.addWidget(self.rule_export_button)
        self.rule_add_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.rule_add_button.setObjectName("rule_add_button")
        self.horizontalLayout_2.addWidget(self.rule_add_button)
        self.rule_edit_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.rule_edit_button.setObjectName("rule_edit_button")
        self.horizontalLayout_2.addWidget(self.rule_edit_button)
        self.rule_delete_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.rule_delete_button.setObjectName("rule_delete_button")
        self.horizontalLayout_2.addWidget(self.rule_delete_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout.addWidget(self.rules_group_box, 0, 1, 1, 1)
        self.hits_group_box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hits_group_box.sizePolicy().hasHeightForWidth())
        self.hits_group_box.setSizePolicy(sizePolicy)
        self.hits_group_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hits_group_box.setObjectName("hits_group_box")
        self.layoutWidget2 = QtWidgets.QWidget(self.hits_group_box)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 40, 700, 400))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.export_results_button = QtWidgets.QPushButton(self.layoutWidget2)
        self.export_results_button.setObjectName("export_results_button")
        self.gridLayout_2.addWidget(self.export_results_button, 1, 0, 1, 1)
        self.hits_list_view = QtWidgets.QListWidget(self.layoutWidget2)
        self.hits_list_view.setObjectName("hits_list_view")
        self.gridLayout_2.addWidget(self.hits_list_view, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.hits_group_box, 1, 1, 1, 1)
        PanelWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PanelWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        PanelWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PanelWindow)
        self.statusbar.setObjectName("statusbar")
        PanelWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(PanelWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(PanelWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtGui.QAction(PanelWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(PanelWindow)
        self.config_tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PanelWindow)

    def retranslateUi(self, PanelWindow):
        _translate = QtCore.QCoreApplication.translate
        PanelWindow.setWindowTitle(_translate("PanelWindow", "Main Panel | SpiderMatch"))
        self.config_group_box.setTitle(_translate("PanelWindow", "Configuracion"))
        self.label.setText(_translate("PanelWindow", "Pais:"))
        self.country_input.setText(_translate("PanelWindow", "CL"))
        self.label_4.setText(_translate("PanelWindow", "Dominio:"))
        self.domain_input.setText(_translate("PanelWindow", "google.cl"))
        self.label_2.setText(_translate("PanelWindow", "Lenguaje:"))
        self.language_input.setText(_translate("PanelWindow", "es-419"))
        self.label_3.setText(_translate("PanelWindow", "Limite de Resultados (profundidad):"))
        self.label_5.setText(_translate("PanelWindow", "Granularidad (meses):"))
        self.granularity_input.setSuffix(_translate("PanelWindow", " mes(es)"))
        self.config_tabs.setTabText(self.config_tabs.indexOf(self.searchTab), _translate("PanelWindow", "Busqueda"))
        self.start_search_button.setText(_translate("PanelWindow", "Comenzar busqueda"))
        self.sites_group_box.setTitle(_translate("PanelWindow", "Sitios y Fuentes (0)"))
        self.site_import_button.setText(_translate("PanelWindow", "Importar"))
        self.site_export_button.setText(_translate("PanelWindow", "Exportar"))
        self.site_add_button.setText(_translate("PanelWindow", "Agregar"))
        self.site_delete_button.setText(_translate("PanelWindow", "Eliminar"))
        self.rules_group_box.setTitle(_translate("PanelWindow", "Reglas de Busqueda (0)"))
        self.rule_import_button.setText(_translate("PanelWindow", "Importar"))
        self.rule_export_button.setText(_translate("PanelWindow", "Exportar"))
        self.rule_add_button.setText(_translate("PanelWindow", "Agregar"))
        self.rule_edit_button.setText(_translate("PanelWindow", "Editar"))
        self.rule_delete_button.setText(_translate("PanelWindow", "Eliminar"))
        self.hits_group_box.setTitle(_translate("PanelWindow", "Resultados (0)"))
        self.export_results_button.setText(_translate("PanelWindow", "Exportar"))
        self.menuFile.setTitle(_translate("PanelWindow", "Archivo"))
        self.actionOpen.setText(_translate("PanelWindow", "Abrir"))
        self.actionSave.setText(_translate("PanelWindow", "Guardar"))
        self.actionSave_as.setText(_translate("PanelWindow", "Guardar como"))