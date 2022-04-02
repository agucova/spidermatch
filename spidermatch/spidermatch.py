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
        self.site_list: list[str] = []
        self.rule_list: list[str] = []

        # Load the UI
        uic.loadUi("windows/panel.ui", self)

        # Site and rule list signals
        self.site_import_button.clicked.connect(self.import_sites)
        self.site_export_button.clicked.connect(self.export_sites)
        self.site_add_button.clicked.connect(self.add_site)
        self.site_delete_button.clicked.connect(self.delete_site)
        self.rule_import_button.clicked.connect(self.import_rules)
        self.rule_export_button.clicked.connect(self.export_rules)
        self.rule_add_button.clicked.connect(self.add_rule)
        self.rule_delete_button.clicked.connect(self.delete_rule)

        # Domain validation regex
        self.domain_validator = re.compile(
            r"\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b$"
        )

        self.show()

    def update_site_list(self):
        self.site_list_view.clear()
        self.site_list_view.addItems(self.site_list)

    def update_rule_list(self):
        self.rule_list_view.clear()
        self.rule_list_view.addItems(self.rule_list)

    def import_sites(self):
        # TODO: Add dialogue validation
        file_path, check = QtWidgets.QFileDialog.getOpenFileName(
            self, "Importar sitios", "", "CSV (*.csv)"
        )
        if check:
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                errors = 0
                for i, row in enumerate(reader):
                    # TODO: Define input format
                    if self.domain_validator.match(row[0]):
                        self.site_list.append(row[0])
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "Advertencia",
                            f"Dominio inválido en la línea {i} (saltado). Recuerda no usar http:// o https:// antes del dominio.",
                        )
                        errors += 1
                        if errors >= 3:
                            QtWidgets.QMessageBox.warning(
                                self,
                                "Error",
                                "Demasiados errores. Cancelando importación.",
                            )
                            break
            self.update_site_list()

    def export_sites(self):
        file_path, check = QtWidgets.QFileDialog.getSaveFileName(
            self, "Exportar sitios", "", "CSV (*.csv)"
        )
        if check:
            with open(file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerows(self.site_list)

    def add_site(self):
        site_name, ok = QtWidgets.QInputDialog.getText(
            self, "Agregar sitio", "Dominio:"
        )
        if ok:
            # From the Regular Expressions Cookbook, 2nd Edition by Jan Goyvaerts, Steven Levithan
            if self.domain_validator.match(site_name):
                self.site_list.append(site_name)
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    "Dominio inválido. Recuerda no usar http:// o https:// antes del dominio.",
                )
            self.update_site_list()

    def delete_site(self):
        selected_row = self.site_list_view.currentRow()
        if 0 <= selected_row < len(self.site_list):
            self.site_list.pop(selected_row)
            self.update_site_list()
        else:
            QtWidgets.QMessageBox.warning(
                self, "Error", "No hay sitio seleccionado para eliminar."
            )

    def import_rules(self):
        file_path, check = QtWidgets.QFileDialog.getOpenFileName(
            self, "Importar reglas", "", "CSV (*.csv)"
        )
        if check:
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.rule_list.append(row[0])
            self.update_rule_list()

    def export_rules(self):
        file_path, check = QtWidgets.QFileDialog.getSaveFileName(
            self, "Exportar reglas", "", "CSV (*.csv)"
        )
        if check:
            with open(file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerows(self.rule_list)

    def add_rule(self):
        rule_name, ok = QtWidgets.QInputDialog.getText(self, "Agregar regla", "Regla:")
        if ok and rule_name:
            self.rule_list.append(rule_name)
            self.update_rule_list()

    def delete_rule(self):
        selected_row = self.rule_list_view.currentRow()
        if 0 <= selected_row < len(self.rule_list):
            self.rule_list.pop(selected_row)
            self.update_rule_list()
        else:
            QtWidgets.QMessageBox.warning(
                self, "Error", "No hay regla seleccionada para eliminar."
            )


if __name__ == "__main__":
    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = WelcomeWindow()

    # setup stylesheet
    apply_stylesheet(app, theme="dark_teal.xml")

    # run
    window.show()
    app.exec()
