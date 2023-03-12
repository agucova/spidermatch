# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

from __future__ import annotations

import datetime

import pytest
from beartype import typing
from hypothesis import given
from hypothesis import strategies as st

import spidermatch.lib.entities
from spidermatch.lib.entities import Hit, Rule, SearchParameters

from .helpers import hits, rules


@given(
    title=st.text(),
    url=st.text(),
    position=st.integers(),
    destination=st.text(),
    description=st.text(),
    date=st.one_of(st.none(), st.text()),
)
def test_fuzz_Hit(
    title: str,
    url: str,
    position: int,
    destination: str,
    description: str,
    date: typing.Union[str, None],
) -> None:
    hit = spidermatch.lib.entities.Hit(
        title=title,
        url=url,
        position=position,
        destination=destination,
        description=description,
        date=date,
    )
    assert isinstance(hit.__str__(), str)
    assert isinstance(hit.csv_row(), tuple)


@given(
    name=st.text(),
    query=st.text(),
    from_date=st.one_of(st.none(), st.datetimes()),
    time_delta=st.one_of(
        st.none(),
        st.timedeltas(
            min_value=datetime.timedelta(days=1), max_value=datetime.timedelta(days=365)
        ),
    ),
)
def test_fuzz_Rule(
    name: str,
    query: str,
    from_date: typing.Union[datetime.datetime, None],
    time_delta: typing.Union[datetime.timedelta, None],
) -> None:
    if from_date is not None and time_delta is not None:
        to_date = from_date + time_delta
    else:
        to_date = None

    rule = spidermatch.lib.entities.Rule(
        name=name, query=query, from_date=from_date, to_date=to_date
    )
    rule.time_length
    rule.is_time_constrained
    if rule.is_time_constrained:
        assert rule.date_str() is not None
    else:
        assert rule.date_str() is None

    rule.csv_row()


@given(
    rule=rules(),
    hits=st.lists(hits()),
)
def test_fuzz_RuleResult(
    rule: Rule,
    hits: typing.List[Hit],
) -> None:
    spidermatch.lib.entities.RuleResult(rule=rule, hits=hits)


@given(q=st.text(), hl=st.text(), gl=st.text(), num=st.integers(), tbs=st.text())
def test_fuzz_SearchParameters(q: str, hl: str, gl: str, num: int, tbs: str) -> None:
    sp = spidermatch.lib.entities.SearchParameters(q=q, hl=hl, gl=gl, num=num, tbs=tbs)
    assert isinstance(sp.to_tuple(), tuple)


@given(
    rule=rules(),
    params=st.builds(SearchParameters),
    from_date=st.one_of(st.none(), st.datetimes()),
    to_date=st.one_of(st.none(), st.datetimes()),
)
def test_fuzz_SearchQuery(
    rule: spidermatch.lib.entities.Rule,
    params: spidermatch.lib.entities.SearchParameters,
    from_date: typing.Union[datetime.datetime, None],
    to_date: typing.Union[datetime.datetime, None],
) -> None:
    spidermatch.lib.entities.SearchQuery(
        rule=rule, params=params, from_date=from_date, to_date=to_date
    )


@given(
    from_date=st.one_of(st.none(), st.datetimes()),
    to_date=st.one_of(st.none(), st.datetimes()),
)
def test_fuzz_generate_tbs(
    from_date: typing.Union[datetime.datetime, None],
    to_date: typing.Union[datetime.datetime, None],
) -> None:
    if from_date and to_date and from_date > to_date:
        with pytest.raises(ValueError):
            spidermatch.lib.entities.generate_tbs(from_date=from_date, to_date=to_date)
    else:
        spidermatch.lib.entities.generate_tbs(from_date=from_date, to_date=to_date)


@given(iter=st.lists(st.one_of([st.integers(), st.text()])), n_parts=st.integers())
def test_fuzz_split(iter, n_parts: int) -> None:
    spidermatch.lib.entities.split(iter=iter, n_parts=n_parts)
    spidermatch.lib.entities.split(iter=iter, n_parts=n_parts)
