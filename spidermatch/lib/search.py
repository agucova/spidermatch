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
    print("Searching for", rule)
    generated_parameters = params.generate_params(rule, from_date, to_date)
    print("Generated parameters: ", generated_parameters)
    response = client.search(generated_parameters)
    if response.get("error"):
        print("Error:", response["error"])
        raise (Exception(response["error"]))

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

    # return [
    #     Hit("Ejemplo 1", "https://www.google.com", 1, "https://www.google.com", "Ejemplo 1", ""),
    #     Hit("Ejemplo 2", "https://www.google.com", 2, "https://www.google.com", "Ejemplo 2", ""),
    #     Hit("Ejemplo 3", "https://www.google.com", 3, "https://www.google.com", "Ejemplo 3", ""),
    # ]


def search_rules(client: zenserp.Client, rules: list[Rule], params: SearchParameters):
    """
    Search for a query in a domain.
    """

    for i, rule in enumerate(rules):
        if rule.from_date and rule.to_date:
            assert rule.time_length
            if rule.time_length > params.granularity:
                windows = calculate_windows(
                    rule.from_date, rule.to_date, params.granularity
                )
                for window in windows:
                    yield (i, RuleResult(rule, search(client, rule, params, window[0], window[1])))
            else:
                hit_results: list[Hit] = search(client, rule, params)
                yield (i, RuleResult(rule, hit_results))
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
