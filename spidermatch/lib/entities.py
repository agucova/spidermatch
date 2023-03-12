from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import NamedTuple

from beartype import typing

from spidermatch.lib.helpers import generate_tbs, split


@dataclass
class Rule:
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
    def is_time_constrained(self) -> bool:
        return bool(self.from_date or self.to_date)

    def date_str(self):
        if self.from_date and self.to_date:
            return (
                f"{self.from_date.strftime('%m/%Y')} a {self.to_date.strftime('%m/%Y')}"
            )
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

    def __post_init__(self):
        if (self.from_date and self.to_date) and (self.from_date > self.to_date):
            raise ValueError("Start date must be before end date")


class RuleTooLong(ValueError):
    def __init__(self, rule: Rule):
        self.rule = rule
        self.message = (
            f"La regla {self.rule} es demasiado larga. "
            "Prueba dividiéndola en reglas más pequeñas "
            "o disminuyendo la cantidad de dominios."
        )
        super().__init__(self.message)


class SearchParameters(NamedTuple):
    """Parameters for a specific query as sent to the API."""

    # (Yes, this could have been a type alias)

    # Query
    q: str
    # Host language
    hl: str
    # Country code
    gl: str
    # Number of results
    num: int
    # Time-based search
    tbs: str

    def to_tuple(self):
        return (
            ("q", self.q),
            ("hl", self.hl),
            ("gl", self.gl),
            ("num", self.num),
            ("tbs", self.tbs),
        )


class SearchConfig:
    """
    General configuration parameters used for searching incidents
    """

    def __init__(
        self,
        country: str = "CL",
        language: str = "es",
        domain: str = "google.cl",
        limit: int = 10,
        granularity: timedelta = timedelta(days=180),
        sites: typing.List[str] | None = None,
    ):
        self.country = country.upper()
        self.language = language.lower()
        self.domain = domain.lower()
        self.limit = limit
        self.granularity = granularity
        self.sites = sites

    def generate_params(
        self,
        rule: Rule,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> typing.List[SearchParameters]:
        from_date = from_date if from_date else rule.from_date
        to_date = to_date if to_date else rule.to_date
        query = rule.query

        if self.sites:
            query += " site:" + " OR site:".join(self.sites)

        if len(query) <= 500:
            # or count_terms(query) <= 32
            # If the query is within the target length
            query_params = SearchParameters(
                query,
                self.language,
                self.country,
                self.limit,
                generate_tbs(from_date, to_date),
            )

            return [query_params]
        else:
            assert (
                self.sites
            ), "Sites must be specified to split queries. Possibly not implemented."
            # Break up query into the least queries possible
            # Yeah, this is done via exhaustive search, but speed doesn't
            # seem to be an issue.
            query_params = [query]
            split_into = 2
            while max(len(q) for q in query_params) > 500:
                if split_into > len(self.sites):
                    raise RuleTooLong(rule)
                site_groups = split(self.sites, split_into)
                query_params = []
                for site_group in site_groups:
                    query_group: str = rule.query
                    if site_group:
                        query_group += " site:" + " OR site:".join(site_group)
                    query_params.append(query_group)
                split_into += 1

            # Here we wrap the queries into their corresponding
            # search parameter objects.
            query_params = [
                SearchParameters(
                    param,
                    self.language,
                    self.country,
                    self.limit,
                    generate_tbs(from_date, to_date),
                )
                for param in query_params
            ]

            return query_params


@dataclass(frozen=True)
class SearchQuery:
    rule: Rule
    params: SearchParameters
    from_date: datetime | None = None
    to_date: datetime | None = None


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
        return (
            f"{self.title} "
            f"({self.description[:60] + ('...' if len(self.description) > 60 else '')})"
        )

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
    hits: typing.List[Hit]
    hits: typing.List[Hit]
