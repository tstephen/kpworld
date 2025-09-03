
def _as_zulu(dt):
    if dt is None:
        return None
    return dt.isoformat(timespec='seconds').replace('+00:00', 'Z') if dt.tzinfo else dt.isoformat(timespec='seconds') + 'Z'
