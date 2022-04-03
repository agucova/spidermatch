from dataclasses import dataclass
from datetime import datetime, timedelta

from spidermatch.lib.helpers import calculate_windows, generate_tbs


@dataclass
class Rule():
    """
    A rule is a search query for a specific time period.
    """

    name: str
    query: str
    from_date: datetime | None = None
    to_date: datetime | None = None

    @property
    def time_length(self) -> timedelta | None:
        if self.from_date and self.to_date:
            return self.to_date - self.from_date
        elif self.from_date:
            return datetime.now() - self.from_date
        elif self.to_date:
            return self.to_date - datetime.now()
        else:
            return None

    @property
    def is_time_constrained(self):
        return bool(self.from_date or self.to_date)

    def date_str(self):
        if self.from_date and self.to_date:
            return f"{self.from_date.strftime('%-m/%Y')} a {self.to_date.strftime('%-m/%Y')}"
        elif self.from_date:
            return f"desde {self.from_date.strftime('%m/%Y')}"
        elif self.to_date:
            return f"hasta {self.to_date.strftime('%m/%Y')}"
        else:
            return None

    def __str__(self):
        if self.from_date or self.to_date:
            return f"{self.name} ({self.date_str()})"
        else:
            return self.name

    def csv_row(self):
        return (
            self.name,
            self.query,
            self.from_date.isoformat() if self.from_date else "",
            self.to_date.isoformat() if self.to_date else "",
        )


class SearchParameters:
    """
    Set of parameters used for searching incidents
    """

    def __init__(
        self,
        country: str = "CL",
        language: str = "es",
        domain: str = "google.cl",
        limit: int = 10,
        granularity: timedelta = timedelta(days=180),
        sites: list[str] | None = None,
    ):
        self.country = country.upper()
        self.language = language.lower()
        self.domain = domain.lower()
        self.limit = limit
        self.granularity = granularity
        self.sites = sites

    def generate_params(self, rule: Rule, from_date: datetime | None = None, to_date: datetime | None = None):
        from_date = from_date if from_date else rule.from_date
        to_date = to_date if to_date else rule.to_date

        query = rule.query

        if self.sites:
            query += " site:" + " OR site:".join(self.sites)

        params = (
            ("q", query),
            ("hl", self.language),
            ("gl", self.country),
            ("num", self.limit),
            ("tbs", generate_tbs(from_date, to_date))
        )

        return params


@dataclass(frozen=True)
class Hit:
    """Hit from a search result."""

    title: str
    url: str
    position: int
    destination: str
    description: str
    date: str | None

    def __str__(self):
        return f"{self.title} ({self.description[:60] + ('...' if len(self.description) > 60 else '')})"

    def csv_row(self):
        return (
            self.title,
            self.url,
            self.position,
            self.destination,
            self.description,
            self.date if self.date else "",
        )


@dataclass(frozen=True)
class RuleResult:
    """
    Result of a search for a rule.
    """

    rule: Rule
    hits: list[Hit]
