from __future__ import annotations

from datetime import date, datetime, timedelta

from beartype import typing


def generate_tbs(from_date: datetime | None, to_date: datetime | None) -> str:
    if from_date and to_date and (from_date > to_date):
        raise ValueError("from_date must be before to_date")

    tbs = ""
    if from_date or to_date:
        tbs = "cdr:1"
    if from_date:
        from_day = int(from_date.strftime("%d"))
        from_month = int(from_date.strftime("%m"))

        tbs += "," + "cd_min:" + from_date.strftime(f"{from_month}/{from_day}/%Y")
    if to_date:
        to_day = int(to_date.strftime("%d"))
        to_month = int(to_date.strftime("%m"))
        tbs += "," + "cd_max:" + to_date.strftime(f"{to_month}/{to_day}/%Y")
    return tbs


def calculate_windows(
    from_date: date, to_date: date, granularity: timedelta
) -> typing.List[typing.Tuple[date | datetime, date | datetime]]:
    """Divide a time period into windows of a given granularity."""
    if to_date - from_date < timedelta(days=1):
        raise ValueError("from_date must be before to_date")
    if to_date - from_date < granularity:
        raise ValueError("granularity must be smaller than the time period")
    if granularity.days < 1:
        raise ValueError("granularity must be at least 1 day")

    window_size = granularity.days
    windows = []
    for i in range(0, (to_date - from_date).days, window_size):
        windows.append(
            (from_date + timedelta(days=i), from_date + timedelta(days=i + window_size))
        )
    if to_date - windows[-1][1] > timedelta(days=14):
        windows.append((windows[-1][1], to_date))
    else:
        windows[-1] = (windows[-1][0], to_date)

    return windows


def split(iter: list, n_parts: int):
    """Splits a sequence into n parts"""
    if n_parts == 1:
        return [iter]
    if n_parts == 0:
        return []

    k, m = divmod(len(iter), n_parts)
    return (
        iter[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n_parts)
    )


def count_terms(text: str):
    """Count the number of words in a given string."""
    return len(text.strip().split(" OR "))
    return len(text.strip().split(" OR "))
