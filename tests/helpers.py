from datetime import timedelta

from hypothesis import strategies as st

from spidermatch.lib.entities import Rule


@st.composite
def rules(draw):
    name = draw(st.text())
    query = draw(st.text())
    from_date = draw(st.one_of(st.none(), st.datetimes()))
    time_delta = draw(
        st.one_of(
            st.none(),
            st.timedeltas(min_value=timedelta(days=1), max_value=timedelta(days=365)),
        )
    )
    if from_date is not None and time_delta is not None:
        to_date = from_date + time_delta
    else:
        to_date = None

    return Rule(name=name, query=query, from_date=from_date, to_date=to_date)
