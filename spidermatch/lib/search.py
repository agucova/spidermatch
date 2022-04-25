from __future__ import annotations
import zenserp
from spidermatch.lib.entities import (
    Rule,
    RuleResult,
    SearchConfig,
    Hit,
    SearchParameters,
    SearchQuery,
)
from spidermatch.lib.helpers import calculate_windows
from datetime import datetime
from beartype import beartype

# The high-level view of this is that
# 1. We generate a search plan that automatically creates all
# the queries needed to search for all the rules
# 2. The (UI) search workers dispatchs each search based


@beartype
def generate_search_plan(rules: list[Rule], config: SearchConfig) -> list[SearchQuery]:
    """
    Generate the list of queries needed to be run for a given set of rules and a config.

    We automatically split queries in their temporal space by their granularity, and split them by length if necessary to satisfy API constraints.
    """

    search_plan: list[SearchQuery] = []
    for rule in rules:
        if rule.from_date and rule.to_date:
            assert rule.time_length
            if rule.time_length > config.granularity:
                windows = calculate_windows(
                    rule.from_date, rule.to_date, config.granularity
                )
                for from_date, to_date in windows:
                    # This is were we split into multiple queries
                    # if maximum query length is exceeded
                    params = config.generate_params(rule, from_date, to_date)
                    # Each item in params is a distinct set of query parameters for a specific search
                    search_plan.extend(
                        SearchQuery(rule, param, from_date, to_date) for param in params
                    )

            else:
                # This is the case were only have one set of searches to do
                # in our temporal space, however this doesn't guarantee
                # one search, because length splits may happen
                params = config.generate_params(rule, None, None)
                search_plan.extend(
                    SearchQuery(rule, param, None, None) for param in params
                )
        else:
            raise (
                NotImplementedError(
                    "Rule must have from_date and to_date. Not implemented yet."
                )
            )

    return search_plan


@beartype
def _search(
    client: zenserp.Client,
    rule: Rule,
    params: SearchParameters,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
) -> list[Hit]:
    """
    Search for a query in a domain.
    """
    response = client.search(params.to_tuple())
    print(response)
    if response.get("error"):
        print("Error:", response["error"])
        raise (ValueError(response["error"]))

    period_results = response.get("organic")

    if period_results is None:
        print("No results found, skipping.")
        return []

    print(period_results)

    hits: list[Hit] = []
    for hit in period_results:
        if hit.get("questions") or hit.get("news"):
            continue

        if not hit.get("title"):
            print("Found hit without title, attributes: ", hit.keys())
            print("(Skipping...)")
            continue

        hits.append(
            Hit(
                title=hit["title"],
                url=hit["url"],
                position=hit["position"],
                destination=hit["destination"],
                description=hit["description"],
                date=hit.get("date"),
            )
        )

    return hits


@beartype
def search(query: SearchQuery, client: zenserp.Client) -> RuleResult:
    """
    Search using a SearchQuery object. High-level interface.
    """
    hits = _search(client, query.rule, query.params, query.from_date, query.to_date)
    return RuleResult(query.rule, hits)


@beartype
def get_remaining_requests(client: zenserp.Client) -> int:
    """
    Get the number of remaining requests.
    """
    return client.status()["remaining_requests"]
