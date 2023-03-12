from beartype import beartype, typing
from PyQt6.QtCore import QThread, pyqtSignal
from zenserp import Client

from spidermatch.lib.entities import Rule, RuleResult, RuleTooLong, SearchConfig
from spidermatch.lib.search import generate_search_plan, search


class SearchWorker(QThread):
    configure_progress_bar = pyqtSignal(int, int)
    progress = pyqtSignal(int, RuleResult)
    error = pyqtSignal(str)

    @beartype
    def __init__(self, client: Client, config: SearchConfig, rules: typing.List[Rule]):
        super().__init__()
        self.client = client
        self.params = config
        self.rules = rules

    def run(self):
        try:
            search_plan = generate_search_plan(self.rules, self.params)
        except RuleTooLong as e:
            self.error.emit(str(e))
            return None

        self.configure_progress_bar.emit(0, len(search_plan) - 1)
        for i, query in enumerate(search_plan):
            try:
                self.progress.emit(i, search(query, self.client))
            except Exception as e:
                self.error.emit(str(e))
