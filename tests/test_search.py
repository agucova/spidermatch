# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

from __future__ import annotations

import datetime

import pytest
from hypothesis import assume, given
from hypothesis import provisional as prov
from hypothesis import strategies as st

import spidermatch.lib.entities
import spidermatch.lib.search
from spidermatch.lib.search import SearchConfig

from .helpers import rules


@given(
    from_date=st.dates(),
    time_delta=st.timedeltas(
        min_value=datetime.timedelta(weeks=8), max_value=datetime.timedelta(weeks=80)
    ),
    granularity=st.timedeltas(
        min_value=datetime.timedelta(weeks=2),
        max_value=datetime.timedelta(weeks=8),
    ),
)
def test_fuzz_calculate_windows(
    from_date: datetime.date,
    time_delta: datetime.timedelta,
    granularity: datetime.timedelta,
) -> None:
    assume(time_delta > granularity)
    to_date = from_date + time_delta
    spidermatch.lib.search.calculate_windows(
        from_date=from_date, to_date=to_date, granularity=granularity
    )


@given(
    rules=st.lists(rules()),
    config=st.builds(
        SearchConfig,
        country=st.one_of(st.just("CL"), st.text()),
        domain=st.one_of(st.just("google.cl"), st.text()),
        granularity=st.one_of(
            st.just(datetime.timedelta(days=180)),
            st.timedeltas(
                min_value=datetime.timedelta(days=30),
                max_value=datetime.timedelta(days=365),
            ),
        ),
        language=st.one_of(st.just("es"), st.text()),
        limit=st.one_of(st.just(10), st.integers()),
        sites=st.one_of(st.none(), st.one_of(st.none(), st.lists(prov.domains()))),
    ),
)
def test_fuzz_generate_search_plan(
    rules: list[spidermatch.lib.entities.Rule],
    config: spidermatch.lib.entities.SearchConfig,
) -> None:

    if any(rule.from_date is None for rule in rules) or any(
        rule.to_date is None for rule in rules
    ):
        with pytest.raises(NotImplementedError):
            spidermatch.lib.search.generate_search_plan(rules=rules, config=config)
    else:
        sp = spidermatch.lib.search.generate_search_plan(rules=rules, config=config)
        assert isinstance(sp, list)
