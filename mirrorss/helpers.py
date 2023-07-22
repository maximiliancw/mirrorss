from datetime import datetime
from validators import url as check_url, ValidationFailure
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def get_random_user_agent() -> str:
    software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    return user_agent_rotator.get_random_user_agent()

def is_valid_url(s: str) -> bool:
    result = check_url(s)
    if isinstance(result, ValidationFailure):
        return False
    return True

def less_than_x_hours_ago(then: float, hours: int) -> bool:
    now = datetime.now().timestamp()
    return (now - then) < hours * 3600