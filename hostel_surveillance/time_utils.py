from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
    IST = ZoneInfo('Asia/Kolkata')
except Exception:
    IST = timezone(timedelta(hours=5, minutes=30))


def now_ist():
    return datetime.now(IST)


def ist_timestamp():
    return now_ist().isoformat(timespec='seconds')


def ist_display(value, fmt='%Y-%m-%d %H:%M:%S'):
    if not value:
        return ''

    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value)
        except ValueError:
            try:
                dt = datetime.fromisoformat(value.replace(' ', 'T'))
            except ValueError:
                return value
    else:
        dt = value

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST)

    return dt.astimezone(IST).strftime(fmt)
