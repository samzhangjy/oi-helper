import os
import pickle
import time

import click
import requests
from psutil._common import bytes2human
from oihelper.submitter import Record, RecordStatus, Submitter

from .common import CONFIG_DIR, STATUS_COLORS, abort_with_error


def get_session() -> requests.Session:
    session_path = f"{CONFIG_DIR}/session.pickle"
    if not os.path.exists(session_path):
        return None
    return pickle.load(open(session_path, "rb"))


def print_record(record: Record) -> None:
    if record["status"] == RecordStatus.COMPILING:
        click.echo(click.style("Compiling...", bold=True, fg="blue"))
        return
    if record["status"] == RecordStatus.CE:
        click.echo(click.style(record["msg"], bold=True, fg="red"))
        return
    for subtask_idx, subtask in enumerate(record["subtasks"], 1):
        click.echo(
            click.style(f"Subtask {subtask_idx}: ")
            + click.style(
                subtask["status"],
                bold=True,
                fg=STATUS_COLORS.get(subtask["status"], STATUS_COLORS["UKE"]),
            )
            + f" / {subtask['time'] / 1000}s / {bytes2human(subtask['memory'] * 1024)}"
        )
        for testcase in subtask["testcases"]:
            additional_details = click.style("No details.", fg="black")
            if testcase["details"] is not None:
                additional_details = testcase["details"]
            click.echo(
                "  "
                + click.style(f"#{testcase['id']}: ", bold=True, fg="blue")
                + click.style(
                    testcase["status"],
                    bold=True,
                    fg=STATUS_COLORS.get(testcase["status"], STATUS_COLORS["UKE"]),
                )
                + f" / {testcase['time_cost'] / 1000}s / {bytes2human(testcase['memory_cost'] * 1000)} / {additional_details}"
            )
    click.echo(
        "Status: "
        + click.style(
            "Accepted" if record["accepted"] else "Unaccepted",
            bold=True,
            fg=STATUS_COLORS.get("AC" if record["accepted"] else "WA"),
        )
        + f" / {record['score']}pts / {record['total_time'] / 1000}s / {bytes2human(record['total_memory'] * 1024)}"
    )


@click.command()
@click.argument("path", required=True)
@click.option("--pid", default=None, help="Problem id.")
def submit(path: str, pid: str) -> None:
    """Submit a solution to Luogu."""
    path = os.path.abspath(path)
    if pid is None:
        pid = path.rsplit("/", 1)[-1].split(".", 1)[0]
    session = get_session()
    if session is None:
        abort_with_error(
            "No login information found. Please login by using the `login` command."
        )
    submitter = Submitter(session)
    rid = submitter.submit(pid, open(path, "r").read())
    click.echo(
        click.style(f"Solution submitted with record ID {rid}.", bold=True, fg="blue")
    )
    click.echo(click.style("Compiling...", bold=True))
    record = submitter.get_record(rid)
    while record["status"] == RecordStatus.COMPILING:
        record = submitter.get_record(rid)
        time.sleep(1)
    if record["status"] != RecordStatus.CE:
        click.echo(click.style("Compiled successfully.", bold=True))
    print_record(record)


@click.command()
@click.argument("rid", required=True)
def record(rid: str) -> None:
    """Get a submition record by ID."""
    session = get_session()
    if session is None:
        abort_with_error(
            "No login information found. Please login by using the `login` command."
        )
    submitter = Submitter(session)
    record = submitter.get_record(rid)
    print_record(record)
