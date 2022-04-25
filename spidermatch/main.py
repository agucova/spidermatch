from __future__ import annotations
from datetime import datetime, timedelta

import re
import sys
import csv
from PyQt6 import QtWidgets, uic
from qt_material import apply_stylesheet
from spidermatch.lib.entities import Hit, Rule, RuleResult, SearchParameters
from spidermatch.worker import SearchWorker
from zenserp import Client


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
            self.panel = PanelWindow(self.api_token)
            self.close()
        else:
            self.api_token_input.setText("")
            self.api_token_input.setPlaceholderText("Token inválido")
            QtWidgets.QMessageBox.warning(self, "Error", "Token inválido")


class PanelWindow(QtWidgets.QMainWindow):
    def __init__(self, api_token: str):
        super(PanelWindow, self).__init__()

        # Site and rule list
        self.site_list: list[str] = []
        self.rule_list: list[Rule] = []
        self.rule_result_list: list[RuleResult] = []

        # Load the UI
        uic.loadUi("windows/panel.ui", self)

        # Store API Token
        self.api_token = api_token

        # Site and rule list signals
        self.site_import_button.clicked.connect(self.import_sites)
        self.site_export_button.clicked.connect(self.export_sites)
        self.site_add_button.clicked.connect(self.add_site)
        self.site_delete_button.clicked.connect(self.delete_site)
        self.rule_import_button.clicked.connect(self.import_rules)
        self.rule_export_button.clicked.connect(self.export_rules)
        self.rule_add_button.clicked.connect(self.add_rule)
        self.rule_list_view.doubleClicked.connect(self.edit_rule)
        self.rule_edit_button.clicked.connect(self.edit_rule)
        self.rule_delete_button.clicked.connect(self.delete_rule)

        # Search buttons
        self.start_search_button.clicked.connect(self.start_search)

        # Results list
        self.export_results_button.clicked.connect(self.export_results)

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
        self.rule_list_view.addItems(str(rule) for rule in self.rule_list)

    def update_hits_list(self):
        self.hits_list_view.clear()
        for rule_result in self.rule_result_list:
            self.hits_list_view.addItems(str(hit) for hit in rule_result.hits)

    def import_sites(self):
        # TODO: Add dialogue validation
        file_path, check = QtWidgets.QFileDialog.getOpenFileName(
            self, "Importar sitios", "", "CSV (*.csv)"
        )
        if check:
            with open(file_path, "r") as f:
                # Sniff CSV patterns
                try:
                    sniffer = csv.Sniffer()
                    dialect = sniffer.sniff(f.read(1024))
                    f.seek(0)
                    has_header = sniffer.has_header(f.read(1024))
                    f.seek(0)

                    # Instantiate the reader to actually read the CSV
                    reader = csv.reader(f, dialect)
                except csv.Error:
                    f.seek(0)
                    reader = csv.reader(f)
                    has_header = True

                errors = 0
                for i, row in enumerate(reader):
                    if i == 0 and has_header:
                        continue

                    if self.domain_validator.match(row[0]):
                        self.site_list.append(row[0])
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "Advertencia",
                            f"Dominio inválido en la línea {i + 1} (saltado). Recuerda no usar http:// o https:// antes del dominio.",
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
                writer.writerow(("domain",))
                writer.writerows(((row,) for row in self.site_list))

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
                try:
                    # Sniff CSV patterns
                    sniffer = csv.Sniffer()
                    dialect = sniffer.sniff(f.read(1024))
                    f.seek(0)
                    has_header = sniffer.has_header(f.read(1024))
                    f.seek(0)

                    # Read the actual CSV
                    reader = csv.reader(f, dialect)
                except csv.Error:
                    f.seek(0)
                    reader = csv.reader(f)
                    has_header = True

                for i, row in enumerate(reader):
                    if i == 0 and has_header:
                        continue
                    self.rule_list.append(
                        Rule(
                            row[0],
                            row[1],
                            datetime.fromisoformat(row[2]),
                            datetime.fromisoformat(row[3]),
                        )
                    )
            self.update_rule_list()

    def export_rules(self):
        file_path, check = QtWidgets.QFileDialog.getSaveFileName(
            self, "Exportar reglas", "", "CSV (*.csv)"
        )
        if check:
            with open(file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(("name", "query", "from_date", "to_date"))
                writer.writerows(rule.csv_row() for rule in self.rule_list)

    def add_rule(self):
        dialog = RuleDialog()
        if dialog.exec():
            rule = Rule(
                dialog.name_input.text(),
                dialog.query_input.toPlainText(),
                dialog.from_input.date().toPyDate(),
                dialog.to_input.date().toPyDate(),
            )
            self.rule_list.append(rule)
            self.update_rule_list()

    def edit_rule(self):
        selected_row = self.rule_list_view.currentRow()
        if 0 <= selected_row < len(self.rule_list):
            dialog = RuleDialog()
            dialog.name_input.setText(self.rule_list[selected_row].name)
            dialog.query_input.setPlainText(self.rule_list[selected_row].query)
            dialog.from_input.setDate(self.rule_list[selected_row].from_date)
            dialog.to_input.setDate(self.rule_list[selected_row].to_date)
            if dialog.exec():
                self.rule_list[selected_row] = Rule(
                    dialog.name_input.text(),
                    dialog.query_input.toPlainText(),
                    dialog.from_input.date().toPyDate(),
                    dialog.to_input.date().toPyDate(),
                )
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

    def validate_config(self) -> bool:
        try:
            assert len(self.country_input.text()) == 2
            assert len(self.language_input.text()) >= 2
            assert len(self.rule_list) > 0
            assert self.domain_validator.match(self.domain_input.text())
        except AssertionError:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Configuración incompleta o inválida."
            )
            return False
        return True

    def configure_progress_bar(self, minimum: int, maximum: int):
        self.progress_bar.setMinimum(minimum)
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(minimum)

    def receive_search_progress(self, progress: int, result: RuleResult):
        self.progress_bar.setValue(progress)
        if result is not None:
            self.rule_result_list.append(result)
            self.update_hits_list()

    def raise_error(self, error: str):
        QtWidgets.QMessageBox.warning(self, "API Error", error)

    def start_search(self):
        if self.validate_config():
            self.progress_bar.setValue(0)
            client = Client(self.api_token)
            params = SearchParameters(
                self.country_input.text(),
                self.language_input.text(),
                self.domain_input.text(),
                self.limit_input.value(),
                timedelta(days=self.granularity_input.value() * 30),
                self.site_list,
            )
            self.search_thread = SearchWorker(client, params, self.rule_list)
            self.search_thread.progress.connect(self.receive_search_progress)
            self.search_thread.configure_progress_bar.connect(
                self.configure_progress_bar
            )
            self.search_thread.finished.connect(self.search_thread.deleteLater)
            self.search_thread.error.connect(self.raise_error)

            self.search_thread.start()

    def export_results(self):
        file_path, check = QtWidgets.QFileDialog.getSaveFileName(
            self, "Exportar resultados", "", "CSV (*.csv)"
        )
        if check:
            with open(file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(
                    (
                        "rule_name",
                        "title",
                        "url",
                        "position",
                        "destination",
                        "description",
                        "date",
                    )
                )
                for rule_result in self.rule_result_list:
                    name = rule_result.rule.name
                    writer.writerows(
                        (name,) + hit.csv_row() for hit in rule_result.hits
                    )


class RuleDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RuleDialog, self).__init__(parent)

        # Load the UI
        uic.loadUi("windows/rule.ui", self)

        self.show()


if __name__ == "__main__":
    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = WelcomeWindow()

    # setup stylesheet
    apply_stylesheet(app, theme="dark_teal.xml")

    # run
    window.show()
    app.exec()
