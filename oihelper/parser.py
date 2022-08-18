import requests

from .common import USER_AGENT


class LuoguParser(object):
    def __init__(self) -> None:
        super().__init__()

    def parse_problem(self, pid: str):
        response = requests.get(
            f"https://www.luogu.com.cn/problem/{pid.upper()}?_contentOnly=1",
            headers={"User-Agent": USER_AGENT}
        ).json()["currentData"]["problem"]
        testcases: list[list[str, str]] = response["samples"]
        time_limit: int = max(response["limits"]["time"])
        memory_limit: int = max(response["limits"]["memory"])
        return {
            "testcases": testcases,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "pid": pid.upper(),
        }
