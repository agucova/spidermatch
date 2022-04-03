from spidermatch.lib.search import search_rules
from spidermatch.lib.entities import Hit, Rule, RuleResult, SearchParameters
from PyQt6.QtCore import QThread, pyqtSignal
from math import floor
from zenserp import Client

class SearchWorker(QThread):
    progress = pyqtSignal(int, RuleResult)
    error = pyqtSignal(str)

    def __init__(self, client: Client, params: SearchParameters, rules: list[Rule]):
        super().__init__()
        self.client = client
        self.params = params
        self.rules = rules

    def run(self):
        try:
            for i, result in search_rules(self.client, self.rules, self.params):
                self.progress.emit(floor(i / len(self.rules) * 100), result)
        except Exception as e:
            self.error.emit(str(e))

        self.progress.emit(len(self.rules), None)

