from datetime import datetime
from validators import url as check_url, ValidationFailure

def is_valid_url(s: str) -> bool:
    result = check_url(s)
    if isinstance(result, ValidationFailure):
        return False
    return True

def less_than_1h_ago(then: float) -> bool:
    now = datetime.now().timestamp()
    return (now - then) < 3600