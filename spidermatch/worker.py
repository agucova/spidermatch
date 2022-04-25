from spidermatch.lib.search import generate_search_plan, search
from spidermatch.lib.entities import Rule, RuleResult, SearchConfig
from PyQt6.QtCore import QThread, pyqtSignal
from math import floor
from zenserp import Client


class SearchWorker(QThread):
    configure_progress_bar = pyqtSignal(int, int)
    progress = pyqtSignal(int, RuleResult)
    error = pyqtSignal(str)

    def __init__(self, client: Client, config: SearchConfig, rules: list[Rule]):
        super().__init__()
        self.client = client
        self.params = config
        self.rules = rules

    def run(self):
        search_plan = generate_search_plan(self.rules, self.params)
        self.configure_progress_bar.emit(0, len(search_plan) - 1)
        for i, query in enumerate(search_plan):
            try:
                self.progress.emit(i, search(query, self.client))
            except Exception as e:
                self.error.emit(str(e))
