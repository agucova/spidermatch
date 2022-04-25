from __future__ import annotations
import zenserp
from spidermatch.lib.entities import (
    Rule,
    RuleResult,
    SearchParameters,
    Hit,
    SearchQuery,
)
from spidermatch.lib.helpers import calculate_windows
from datetime import datetime


def generate_search_plan(
    rules: list[Rule], params: SearchParameters
) -> list[SearchQuery]:
    """Generate the list of queries needed to be run for a given set of rules and params"""
    search_plan: list[SearchQuery] = []
    for rule in rules:
        if rule.from_date and rule.to_date:
            assert rule.time_length
            if rule.time_length > params.granularity:
                windows = calculate_windows(
                    rule.from_date, rule.to_date, params.granularity
                )
                for from_date, to_date in windows:
                    search_plan.append(SearchQuery(rule, params, from_date, to_date))
            else:
                search_plan.append(SearchQuery(rule, params, None, None))
        else:
            raise (
                NotImplementedError("Rule must have from_date and to_date. Not implemented yet.")
            )

    return search_plan


def _search(
    client: zenserp.Client,
    rule: Rule,
    params: SearchParameters,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
):
    """
    Search for a query in a domain.
    """
    print("Searching for", rule)
    generated_parameters = params.generate_params(rule, from_date, to_date)
    print("Generated parameters: ", generated_parameters)
    response = client.search(generated_parameters)
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


def search(query: SearchQuery, client: zenserp.Client) -> RuleResult:
    """
    Search using a SearchQuery object. High-level interface.
    """
    hits = _search(client, query.rule, query.params, query.from_date, query.to_date)
    return RuleResult(query.rule, hits)


def get_remaining_requests(client: zenserp.Client):
    """
    Get the number of remaining requests.
    """
    return client.status()["remaining_requests"]
