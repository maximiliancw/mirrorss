from validators import url as check_url, ValidationFailure

def is_valid_url(s: str) -> bool:
    result = check_url(s)
    if isinstance(result, ValidationFailure):
        return False
    return True
