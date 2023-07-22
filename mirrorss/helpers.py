from datetime import datetime
from validators import url as check_url, ValidationFailure

def is_valid_url(s: str) -> bool:
    result = check_url(s)
    if isinstance(result, ValidationFailure):
        return False
    return True

def less_than_x_hours_ago(then: float, hours: int) -> bool:
    now = datetime.now().timestamp()
    return (now - then) < hours * 3600