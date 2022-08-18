from enum import Enum
from typing import TypedDict
import requests

from oihelper.auth import AuthenticationHandler
from oihelper.common import USER_AGENT


class Testcase(TypedDict):
    time_cost: int
    memory_cost: int
    details: str | None
    score: float
    status: str
    id: int


class Subtask(TypedDict):
    score: float
    time: int
    memory: int
    testcases: list[Testcase]
    status: str
    id: int


class RecordStatus(Enum):
    COMPILING = 1
    CE = 2
    DONE = 3


class Record(TypedDict):
    score: int
    accepted: bool
    subtasks: list[Subtask]
    total_time: int
    total_memory: int
    status: RecordStatus
    msg: str


class Submitter(object):
    def __init__(self, session: requests.Session) -> None:
        super().__init__()
        self.session = session
        self.auth_handler = AuthenticationHandler(session)

    def submit(self, pid: str, code: str) -> str:
        response = self.session.post(
            f"https://www.luogu.com.cn/fe/api/problem/submit/{pid}",
            json={"code": code},
            headers={
                "User-Agent": USER_AGENT,
                "referer": "https://www.luogu.com.cn/auth/login",
                "X-CSRF-TOKEN": self.auth_handler._get_csrf_token(),
            },
        )
        response.raise_for_status()
        return str(response.json()["rid"])

    def _get_status_type(self, status: int) -> str:
        result = "UKE"
        match status:
            case 4:
                result = "MLE"
            case 5:
                result = "TLE"
            case 6 | 14:
                result = "WA"
            case 7:
                result = "RE"
            case 12:
                result = "AC"
        return result

    def get_record(self, rid: str) -> Record:
        response = self.session.get(
            f"https://www.luogu.com.cn/record/{rid}?_contentOnly=1"
        ).json()["currentData"]["record"]
        record_details = response["detail"]

        if record_details["compileResult"] is None or response.get("score") is None:
            return {"status": RecordStatus.COMPILING}

        if not record_details["compileResult"]["success"]:
            return {
                "status": RecordStatus.CE,
                "msg": f"Compilation failed.\n\n{record_details['compileResult']['message']}",
            }

        result: Record = {
            "subtasks": [],
            "accepted": response["status"] == 12,
            "score": response["score"],
            "total_time": response["time"],
            "total_memory": response["memory"],
            "status": RecordStatus.DONE,
        }

        for idx, subtask in enumerate(record_details["judgeResult"]["subtasks"], 1):
            cur_result: Subtask = {
                "score": subtask["score"],
                "time": subtask["time"],
                "memory": subtask["memory"],
                "testcases": [],
                "status": self._get_status_type(subtask["status"]),
                "id": idx,
            }

            for testcase_id in range(len(subtask["testCases"])):
                testcase = subtask["testCases"][str(testcase_id)]
                cur_testcase: Testcase = {
                    "time_cost": testcase["time"],
                    "memory_cost": testcase["memory"],
                    "details": None,
                    "score": testcase["score"],
                    "id": testcase_id + 1,
                    "status": self._get_status_type(testcase["status"]),
                }
                match testcase["status"]:
                    case 6:
                        cur_testcase["details"] = testcase["description"]
                    case 7:
                        cur_testcase[
                            "details"
                        ] = f"Received signal {testcase['signal']}."
                    case 12:
                        cur_testcase["details"] = testcase["description"]
                cur_result["testcases"].append(cur_testcase)
            result["subtasks"].append(cur_result)

        return result
