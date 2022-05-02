from datetime import datetime, timedelta, date
from beartype import beartype


def generate_tbs(from_date: datetime | None, to_date: datetime | None) -> str:
    tbs = ""
    if from_date or to_date:
        tbs = "cdr:1"
    if from_date:
        tbs += "," + "cd_min:" + from_date.strftime("%-m/%-d/%Y")
    if to_date:
        tbs += "," + "cd_max:" + to_date.strftime("%-m/%-d/%Y")
    return tbs


@beartype
def calculate_windows(
    from_date: date, to_date: date, granularity: timedelta
) -> list[tuple[date | datetime, date | datetime]]:
    """Divide a time period into windows of a given granularity."""
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


def split(iter, n_parts: int):
    """Splits a sequence into n parts"""
    k, m = divmod(len(iter), n_parts)
    return (
        iter[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n_parts)
    )

def count_terms(text: str):
    """Count the number of words in a given string."""
    return len(text.strip().split(" OR "))
