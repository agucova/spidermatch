from datetime import datetime, timedelta


def generate_tbs(from_date: datetime | None, to_date: datetime | None):
    tbs = ""
    if from_date or to_date:
        tbs = "cdr:1"
    if from_date:
        tbs += "," + "cd_min:" + from_date.strftime("%-m/%-d/%Y")
    if to_date:
        tbs += "," + "cd_max:" + to_date.strftime("%-m/%-d/%Y")
    return tbs


def calculate_windows(from_date: datetime, to_date: datetime, granularity: timedelta):
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
