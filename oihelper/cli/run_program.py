import json
import os
import re

import click
from oihelper.judger import Judger

from .common import CONFIG_DIR, CONFIG_FILE, STATUS_COLORS, get_testcase_no, warn


def run_testcases(
    testcases: list[tuple[str, str]],
    judger: Judger,
    max_time: float,
    max_memory: int,
    msg: str = "Running testcase {id} ...",
) -> None:
    for testcase in testcases:
        click.echo(click.style(msg.format(id=testcase[0]), bold=True, fg="blue"))
        result = judger.run_program(
            "./output", testcase[1], testcase[2], max_time, 1024 * 1024 * max_memory
        )

        status_text = click.style(
            result["status"],
            bold=True,
            fg=STATUS_COLORS.get(result["status"], STATUS_COLORS["UKE"]),
        )
        additional_info = click.style("No details.", fg="black")

        match result["status"]:
            case "AC":
                additional_info = f"{round(result['details']['time_cost'], 2)}s / {result['details']['memory_usage']}"
            case "WA":
                additional_info = result["details"]
            case "RE":
                additional_info = result["details"]
            case "TLE":
                additional_info = result["details"]
            case "MLE":
                additional_info = result["details"]

        click.echo(f"  {status_text} / {additional_info}")


def find_local_testcases(prefix: str, testcases_dir: str):
    testcase_inputs = []
    testcase_outputs = []
    testcases = []
    testcase_input_tester = re.compile(f"{prefix}(\d+)?.in")
    testcase_output_tester = re.compile(f"{prefix}(\d+)?.out")
    local_input_tester = re.compile(f"{prefix}-(\d+).in")
    local_output_tester = re.compile(f"{prefix}-(\d+).out")

    for root, dirs, files in os.walk(testcases_dir):
        for filename in files:
            if testcase_input_tester.match(filename) or local_input_tester.match(
                filename
            ):
                testcase_inputs.append(filename)
            elif testcase_output_tester.match(filename) or local_output_tester.match(
                filename
            ):
                testcase_outputs.append(filename)

    testcase_path_prefix = os.path.abspath(testcases_dir)

    for _input in testcase_inputs:
        input_no = get_testcase_no(_input)
        for output in testcase_outputs:
            output_no = get_testcase_no(output)
            if input_no != output_no:
                continue
            testcases.append(
                (
                    input_no,
                    open(os.path.join(testcase_path_prefix, _input)),
                    open(os.path.join(testcase_path_prefix, output)),
                )
            )
            break
    return testcases


@click.command(name="run")
@click.argument("path", type=click.STRING)
@click.option("--name", "-n", default=None, help="Name of program test cases.")
@click.option(
    "--time", "-t", default=1.0, help="Maximum run time for the program in seconds."
)
@click.option(
    "--memory",
    "-m",
    default=128,
    help="Maximum memory usage for the program in megabytes.",
)
@click.option("--testcase", "-T", default="./", help="Path to the testcases directory.")
@click.option("--compiler", "-c", default="g++", help="Path to the compiler.")
def run(
    path: str, name: str | None, time: float, memory: int, testcase: str, compiler: str
):
    """Run the given local file and its testcases."""
    testcase = os.path.abspath(testcase)
    path = os.path.abspath(path)

    problem_id = path.rsplit("/", 1)[-1].split(".", 1)[0]
    if name is None:
        name = problem_id

    judger = Judger(compiler)
    judger.compile_program(path, "./output")

    config: dict[str, dict] = json.load(open(CONFIG_FILE, "r"))

    if config.get(path) is not None:
        cur = config[path]
        samples = find_local_testcases("test", f"{CONFIG_DIR}/{problem_id}")
        run_testcases(
            samples,
            judger,
            cur["time_limit"],
            cur["memory_limit"] / 1024,
            "Running sample {id} ...",
        )
    else:
        warn("No samples found in OI-Helper database.")

    testcases = find_local_testcases(name, testcase)

    if len(testcases) == 0:
        warn(f"No local testcases found in {testcase} .")
    else:
        click.echo(f"Discovered {len(testcases)} local testcases in {testcase} .")

    run_testcases(testcases, judger, time, memory)
