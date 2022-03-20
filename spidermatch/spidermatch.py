from __future__ import annotations

import re
import sys
import csv
from PyQt6 import QtWidgets, uic
from qt_material import apply_stylesheet

class WelcomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        uic.loadUi("windows/welcome.ui", self)
        # Connect the save button to the save_token method
        self.api_save_button.clicked.connect(self.save_token)
        # Set input enter to submit button
        self.api_token_input.returnPressed.connect(self.save_token)
        self.show()

    def save_token(self):
        token_matcher = r"[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"
        self.api_token: str = self.api_token_input.text()
        if self.api_token and re.match(token_matcher, self.api_token):
            self.panel = PanelWindow()
            self.close()
        else:
            self.api_token_input.setText("")
            self.api_token_input.setPlaceholderText("Token inválido")
            QtWidgets.QMessageBox.warning(self, "Error", "Token inválido")

class PanelWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PanelWindow, self).__init__()

        # Site and rule list
        # TODO: Solve undefinition error
        self._site_list: list[str] = []
        self._rule_list: list[str] = []

        # Load the UI
        uic.loadUi("windows/panel.ui", self)

        # Models
        # self.site_list_model = QStandardItemModel(self.site_list_view)
        # self.rule_list_model = QStandardItemModel(self.rule_list_view)
        # self.site_list_view.setModel(self.site_list_model)
        # self.rule_list_view.setModel(self.rule_list_model)

        # Site and rule list signals
        self.site_import_button.clicked.connect(self.import_sites)
        self.site_export_button.clicked.connect(self.export_sites)
        self.rule_import_button.clicked.connect(self.import_rules)
        self.rule_export_button.clicked.connect(self.export_rules)


        self.show()

    @property
    def site_list(self):
        return self._site_list

    @site_list.setter
    def site_list(self, site_list: list[str]):
        self._site_list = site_list
        self.update_site_list()

    @property
    def rule_list(self):
        return self._rule_list

    @rule_list.setter
    def rule_list(self, rule_list: list[str]):
        self._rule_list = rule_list
        self.update_rule_list()

    def update_site_list(self):
        self.site_list_view.clear()
        self.site_list_view.addItems(self.site_list)
        self.site_list_view.update()

    def update_rule_list(self):
        self.rule_list_view.clear()
        self.rule_list_view.addItems(self.site_list)
        self.rule_list_view.update()

    def import_sites(self):
        # TODO: Add dialogue validation
        file_path, check = QtWidgets.QFileDialog.getOpenFileName(self, "Importar sitios", "", "CSV (*.csv)")
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                # TODO: Define input format
                self.site_list.append(row[0])
        self.update_site_list()

    def export_sites(self):
        file_path, check = QtWidgets.QFileDialog.getSaveFileName(self, "Exportar sitios", "", "CSV (*.csv)")
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerows(self.site_list)

    def import_rules(self):
        file_path, check = QtWidgets.QFileDialog.getOpenFileName(self, "Importar reglas", "", "CSV (*.csv)")
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.rule_list.append(row[0])
        self.update_rule_list()

    def export_rules(self):
        file_path, check = QtWidgets.QFileDialog.getSaveFileName(self, "Exportar reglas", "", "CSV (*.csv)")
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerows(self.rule_list)




if __name__ == "__main__":
    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = WelcomeWindow()

    # setup stylesheet
    apply_stylesheet(app, theme="dark_teal.xml")

    # run
    window.show()
    app.exec()
