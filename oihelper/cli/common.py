import os
import pathlib
import re
import click

CONFIG_DIR = os.path.expanduser(f"{pathlib.Path.home()}/oi-helper/")
CONFIG_FILE = pathlib.Path(f"{CONFIG_DIR}/config.json")
STATUS_COLORS = {
    "AC": "green",
    "WA": "red",
    "RE": "magenta",
    "TLE": "cyan",
    "MLE": "yellow",
    "UKE": "blue"
}

def get_testcase_no(testcase: str) -> int:
    testcase_no = 0
    custom_testcase_tester = re.compile("\w+\d+-\d+.\w+")
    if custom_testcase_tester.match(testcase):
        return int(testcase.split("-", 1)[-1].split(".")[0])

    for ch in testcase:
        if ch.isdigit():
            testcase_no = testcase_no * 10 + int(ch)
    return testcase_no


def abort_with_error(msg: str) -> None:
    click.echo(click.style(f"Error: {msg}", bold=True, fg="red"))
    raise click.Abort(msg)

def warn(msg: str) -> None:
    click.echo(click.style(f"Warning: {msg}", bold=True, fg="yellow"))
