from datetime import datetime, timedelta


def expired_time(hour, minute):
    current = datetime.now()
    future = current.replace(hour=hour, minute=minute)
    if future <= current:
        future += timedelta(days=1)
    return int((future - current).total_seconds())
