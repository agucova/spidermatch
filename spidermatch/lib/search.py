import zenserp
from spidermatch.lib.entities import (
    Rule,
    RuleResult,
    SearchParameters,
    Hit,
)
from spidermatch.lib.helpers import calculate_windows
from datetime import datetime


def search(
    client: zenserp.Client,
    rule: Rule,
    params: SearchParameters,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
):
    """
    Search for a query in a domain.
    """
    generated_parameters = params.generate_params(rule, from_date, to_date)
    period_results = client.search(generated_parameters)["organic"]
    return [
        Hit(
            title=hit["title"],
            url=hit["url"],
            position=hit["position"],
            destination=hit["destination"],
            description=hit["description"],
            date=hit.get("date"),
        )
        for hit in period_results
    ]


def search_rules(client: zenserp.Client, rules: list[Rule], params: SearchParameters):
    """
    Search for a query in a domain.
    """

    for rule in rules:
        if rule.from_date and rule.to_date:
            assert rule.time_length
            if rule.time_length > params.granularity:
                period_results: list[Hit] = []
                windows = calculate_windows(
                    rule.from_date, rule.to_date, params.granularity
                )
                for window in windows:
                    period_results.extend(
                        search(client, rule, params, window[0], window[1])
                    )
                yield RuleResult(rule, period_results)
            else:
                hit_results: list[Hit] = search(client, rule, params)
                yield RuleResult(rule, hit_results)
        else:
            raise (
                Exception("Rule must have from_date and to_date. Not implemented yet.")
            )


def get_remaining_requests(client: zenserp.Client):
    """
    Get the number of remaining requests.
    :param client: Zenserp client.
    :return: Number of remaining requests.
    """
    return client.status()["remaining_requests"]
